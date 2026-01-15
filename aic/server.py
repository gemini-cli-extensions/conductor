import asyncio
import os
from mcp.server.fastmcp import FastMCP
from aic.db import init_db, upsert_node, update_edges, mark_dirty
from aic.skeleton import UniversalSkeletonizer
from aic.utils import calculate_hash, resolve_dep_to_path, get_ignore_patterns, should_ignore
from aic.cli import get_context

# Initialize FastMCP server
mcp = FastMCP("aic")

@mcp.tool()
async def aic_index(root_dir: str) -> str:
    """
    Indexes the repository to build a semantic dependency graph.
    Scans for Python files, generates skeletons, and updates the SQLite database.
    
    Args:
        root_dir: The root directory of the repository to index.
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
            # Simple heuristic: check extension or try reading
            try:
                with open(file_path, 'r', encoding='utf-8', errors='strict') as f:
                    content = f.read()
            except UnicodeDecodeError:
                # print(f"Skipping binary file: {rel_path}")
                continue
            except Exception as e:
                print(f"Skipping {rel_path}: {e}")
                continue
                
            current_hash = calculate_hash(content)
            # We skip optimization for now to ensure we always get latest state or implement get_node in db
            # existing = get_node(rel_path)
            # if existing and existing['hash'] == current_hash:
            #     continue
                
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

@mcp.tool()
async def aic_get_file_context(file_path: str) -> str:
    """
    Retrieves the extensive context for a file, including its skeleton and its direct dependencies' skeletons.
    
    Args:
        file_path: Relative path to the file to get context for.
    """
    try:
        return get_context(file_path)
    except Exception as e:
        return f"Error retrieving context for {file_path}: {str(e)}"

@mcp.tool()
async def aic_list_directory(path: str) -> str:
    """
    Lists the files and directories in the specified path.
    
    Args:
        path: The directory path to list.
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

@mcp.tool()
async def aic_run_shell_command(command: str, cwd: str) -> str:
    """
    Executes a shell command.
    
    Args:
        command: The command line string to execute.
        cwd: Current working directory (use "." for current).
    """
    try:
        # Resolve "." to None if needed, or just let shell handle it if we pass it? 
        # asyncio.create_subprocess_shell handles cwd="." fine.
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
    mcp.run()
