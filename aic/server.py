import asyncio
import sys
import json
import logging
import inspect
import os
import traceback
from typing import Any, Callable, Dict, List, Optional

from aic.db import init_db, upsert_node, update_edges, mark_dirty
from aic.skeleton import UniversalSkeletonizer
from aic.utils import calculate_hash, resolve_dep_to_path, get_ignore_patterns, should_ignore
from aic.cli import get_context

# Configure logging to stderr so it doesn't interfere with JSON-RPC on stdout
logging.basicConfig(stream=sys.stderr, level=logging.INFO)
logger = logging.getLogger("aic-server")

class MCPServer:
    def __init__(self, name: str):
        self.name = name
        self.tools: Dict[str, Callable] = {}
        self.tool_schemas: List[Dict[str, Any]] = []

    def tool(self):
        """Decorator to register a function as a tool."""
        def decorator(func: Callable):
            self.register_tool(func)
            return func
        return decorator

    def register_tool(self, func: Callable):
        name = func.__name__
        doc = inspect.getdoc(func) or ""
        sig = inspect.signature(func)
        
        properties = {}
        required = []
        
        for param_name, param in sig.parameters.items():
            param_type = "string"  # Default to string for simplicity in this minimal implementation
            if param.annotation == int:
                param_type = "integer"
            elif param.annotation == bool:
                param_type = "boolean"
                
            properties[param_name] = {
                "type": param_type,
                "description": f"Parameter {param_name}" 
            }
            # Simple heuristic: parameters without defaults are required
            if param.default == inspect.Parameter.empty:
                required.append(param_name)

        schema = {
            "name": name,
            "description": doc,
            "inputSchema": {
                "type": "object",
                "properties": properties,
                "required": required
            }
        }
        
        self.tools[name] = func
        self.tool_schemas.append(schema)
        logger.info(f"Registered tool: {name}")

    async def handle_request(self, request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        method = request.get("method")
        msg_id = request.get("id")
        
        if method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "tools": self.tool_schemas
                }
            }
            
        elif method == "tools/call":
            params = request.get("params", {})
            tool_name = params.get("name")
            tool_args = params.get("arguments", {})
            
            if tool_name not in self.tools:
                return {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "error": {
                        "code": -32601,
                        "message": f"Tool not found: {tool_name}"
                    }
                }
            
            try:
                func = self.tools[tool_name]
                # Check if async
                if inspect.iscoroutinefunction(func):
                    result = await func(**tool_args)
                else:
                    result = func(**tool_args)
                
                return {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": str(result)
                            }
                        ]
                    }
                }
            except Exception as e:
                logger.error(f"Error executing {tool_name}: {traceback.format_exc()}")
                return {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "error": {
                        "code": -32603,
                        "message": f"Internal error: {str(e)}"
                    }
                }
        
        # Handle other MCP lifecycle methods strictly to avoid errors
        elif method == "initialize":
             return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "protocolVersion": "0.1.0",
                    "capabilities": {
                        "tools": {}
                    },
                    "serverInfo": {
                        "name": self.name,
                        "version": "0.1.0"
                    }
                }
            }
        elif method == "notifications/initialized":
             # No response needed for notifications
             return None
             
        return None

    async def run(self):
        logger.info(f"Starting {self.name} server on stdio...")
        
        # We need to read from stdin line by line (JSON-RPC)
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)
        await loop.connect_read_pipe(lambda: protocol, sys.stdin)
        
        while True:
            try:
                line = await reader.readline()
                if not line:
                    break
                    
                message = json.loads(line)
                response = await self.handle_request(message)
                
                if response:
                    sys.stdout.write(json.dumps(response) + "\n")
                    sys.stdout.flush()
                    
            except json.JSONDecodeError:
                logger.error("Failed to decode JSON from stdin")
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                break

server = MCPServer("aic")

@server.tool()
async def aic_index(root_dir: str) -> str:
    """
    Indexes the repository to build a semantic dependency graph.
    Scans for Python files, generates skeletons, and updates the SQLite database.
    """
    init_db()
    skeletonizer = UniversalSkeletonizer()
    indexed_count = 0
    
    # Ensure we use absolute path for walking
    abs_root_dir = os.path.abspath(root_dir)
    ignore_patterns = get_ignore_patterns(abs_root_dir)
    
    for root, dirs, files in os.walk(abs_root_dir):
        # Exclusions
        dirs[:] = [d for d in dirs if not should_ignore(d, ignore_patterns)]
        
        for file in files:
            if should_ignore(file, ignore_patterns):
                continue
                
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, abs_root_dir)
            
            # Skip non-text files to avoid reading binaries
            try:
                with open(file_path, 'r', encoding='utf-8', errors='strict') as f:
                    content = f.read()
            except UnicodeDecodeError:
                continue
            except Exception as e:
                print(f"Skipping {rel_path}: {e}")
                continue
                
            current_hash = calculate_hash(content)
            
            skeleton, dependencies = skeletonizer.skeletonize(content, rel_path)
            upsert_node(rel_path, current_hash, skeleton)
            mark_dirty(rel_path)
            
            # Resolve dependencies to file paths
            resolved_deps = []
            for dep in dependencies:
                resolved = resolve_dep_to_path(dep, rel_path, abs_root_dir)
                if resolved:
                    resolved_deps.append(resolved)
            
            update_edges(rel_path, resolved_deps)
            indexed_count += 1
            
    return f"Successfully indexed {indexed_count} files in {abs_root_dir}"

@server.tool()
async def aic_get_file_context(file_path: str) -> str:
    """
    Retrieves the extensive context for a file, including its skeleton and its direct dependencies' skeletons.
    """
    try:
        return get_context(file_path)
    except Exception as e:
        return f"Error retrieving context for {file_path}: {str(e)}"

@server.tool()
async def aic_list_directory(path: str) -> str:
    """
    Lists the files and directories in the specified path.
    """
    try:
        abs_path = os.path.abspath(path)
        if not os.path.exists(abs_path):
            return f"Error: Path '{path}' not found."
            
        items = []
        for name in os.listdir(abs_path):
             full_path = os.path.join(abs_path, name)
             is_dir = os.path.isdir(full_path)
             items.append(f"{name}{'/' if is_dir else ''}")
        
        return "\n".join(sorted(items))
    except Exception as e:
        return f"Error listing directory '{path}': {str(e)}"

@server.tool()
async def aic_run_shell_command(command: str, cwd: str) -> str:
    """
    Executes a shell command.
    """
    try:
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=cwd
        )
        stdout, stderr = await process.communicate()
        
        output = f"Exit Code: {process.returncode}\n"
        if stdout:
            output += f"\nStandard Output:\n{stdout.decode().strip()}"
        if stderr:
            output += f"\nStandard Error:\n{stderr.decode().strip()}"
            
        return output
    except Exception as e:
        return f"Error executing command: {str(e)}"

if __name__ == "__main__":
    asyncio.run(server.run())