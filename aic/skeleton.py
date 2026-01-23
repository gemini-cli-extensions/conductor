import ast
import os
import re

class PythonSkeletonizer(ast.NodeVisitor):
# ... (rest of PythonSkeletonizer remains the same)
    def __init__(self):
        self.reset()

    def reset(self):
        self.skeleton = []
        self.dependencies = set()
        self.imports = []

    def skeletonize(self, source_code, path):
        self.reset()
        try:
            tree = ast.parse(source_code)
        except Exception as e:
            return f"# BUG: Failed to parse {path}: {str(e)}", set()

        self.visit(tree)
        return "\n".join(self.skeleton), self.dependencies

    def visit_Import(self, node):
        for alias in node.names:
            self.dependencies.add(alias.name)
            self.imports.append(f"import {alias.name}")

    def visit_ImportFrom(self, node):
        module = node.module or ""
        level = node.level
        # Handle relative imports level
        prefix = "." * level if level > 0 else ""
        full_module = prefix + module
        
        for alias in node.names:
            self.dependencies.add(full_module)
            self.imports.append(f"from {full_module} import {alias.name}")

    def visit_ClassDef(self, node):
        # Extract class signature
        self.skeleton.append(f"class {node.name}:")
        docstring = ast.get_docstring(node)
        if docstring:
            self.skeleton.append(f'    """{docstring}"""')
        
        # We don't visit children yet, just let the visitor handle them
        # But we want to indent them
        old_skeleton = self.skeleton
        self.skeleton = []
        self.generic_visit(node)
        inner = self.skeleton
        self.skeleton = old_skeleton
        for line in inner:
            self.skeleton.append(f"    {line}")
        self.skeleton.append("") # Spacer

    def visit_FunctionDef(self, node):
        self._skeletonize_func(node)

    def visit_AsyncFunctionDef(self, node):
        self._skeletonize_func(node, is_async=True)

    def _skeletonize_func(self, node, is_async=False):
        prefix = "async " if is_async else ""
        args = ast.unparse(node.args) if hasattr(ast, 'unparse') else "..."
        returns = f" -> {ast.unparse(node.returns)}" if hasattr(ast, 'unparse') and node.returns else ""
        
        signature = f"{prefix}def {node.name}({args}){returns}:"
        self.skeleton.append(signature)
        
        docstring = ast.get_docstring(node)
        if docstring:
            self.skeleton.append(f'    """{docstring}"""')
        
        # Effects analysis
        effects = self._analyze_effects(node)
        if effects:
            self.skeleton.append(f"    # {effects}")
        
        self.skeleton.append("    ...")
        self.skeleton.append("") # Spacer

    def _analyze_effects(self, node):
        returns = []
        raises = []
        calls = []
        
        for child in ast.walk(node):
            if isinstance(child, ast.Return):
                if child.value:
                    try:
                        returns.append(ast.unparse(child.value))
                    except:
                        returns.append("some_value")
            elif isinstance(child, ast.Raise):
                if child.exc:
                    try:
                        raises.append(ast.unparse(child.exc))
                    except:
                        raises.append("Exception")
            elif isinstance(child, ast.Call):
                try:
                    calls.append(ast.unparse(child.func))
                except:
                    pass
        
        res = []
        if returns: res.append(f"RETURNS: {' | '.join(list(set(returns))[:3])}")
        if raises: res.append(f"RAISES: {' | '.join(list(set(raises))[:3])}")
        if calls: res.append(f"CALLS: {' | '.join(list(set(calls))[:5])}")
        
        return " | ".join(res)

class TypeScriptSkeletonizer:
    def skeletonize(self, source_code, path):
        skeleton = []
        dependencies = set()
        
        # Simple regex for imports
        import_matches = re.findall(r'import\s+.*?\s+from\s+[\'"](.*?)[\'"]', source_code)
        for dep in import_matches:
            dependencies.add(dep)
            
        # Strip comments for processing but keep them in skeleton if they are doc-like
        lines = source_code.splitlines()
        i = 0
        while i < len(lines):
            line = lines[i]
            # Capture imports
            if line.strip().startswith('import '):
                skeleton.append(line)
            # Capture class/interface/function signatures
            elif re.search(r'\b(class|interface|function|enum|type|const|let|async)\b', line):
                # If it looks like a declaration
                if '{' in line or line.strip().endswith(';'):
                    # Basic approach: take the line, if it has '{', add '...' and find matching '}'
                    # This is naive but works for simple cases
                    sig = line.split('{')[0].strip()
                    if sig:
                        skeleton.append(sig + " { ... }")
                else:
                    skeleton.append(line)
            # Capture JSDoc
            elif line.strip().startswith('/**'):
                doc = [line]
                while i + 1 < len(lines) and not lines[i].strip().endswith('*/'):
                    i += 1
                    doc.append(lines[i])
                skeleton.append("\n".join(doc))
            i += 1
            
        return "\n".join(skeleton), dependencies

class GoSkeletonizer:
    def skeletonize(self, source_code, path):
        skeleton = []
        dependencies = set()
        
        # Simple regex for imports
        # Single line: import "fmt"
        # Multi line: import ( "fmt" "os" )
        import_block = re.search(r'import\s*\((.*?)\)', source_code, re.DOTALL)
        if import_block:
            deps = re.findall(r'[\'"](.*?)[\'"]', import_block.group(1))
            dependencies.update(deps)
        
        single_imports = re.findall(r'import\s+[\'"](.*?)[\'"]', source_code)
        dependencies.update(single_imports)

        lines = source_code.splitlines()
        i = 0
        while i < len(lines):
            line = lines[i]
            # Capture package
            if line.strip().startswith('package '):
                skeleton.append(line)
            # Capture func/type/struct/interface
            elif re.search(r'\b(func|type|struct|interface|const|var)\b', line):
                 if '{' in line:
                     sig = line.split('{')[0].strip()
                     skeleton.append(sig + " { ... }")
                 else:
                     skeleton.append(line)
            # Capture comments
            elif line.strip().startswith('//'):
                skeleton.append(line)
            i += 1
            
        return "\n".join(skeleton), dependencies

class UniversalSkeletonizer:
    def __init__(self):
        self.py_skeletonizer = PythonSkeletonizer()
        self.ts_skeletonizer = TypeScriptSkeletonizer()
        self.go_skeletonizer = GoSkeletonizer()

    def skeletonize(self, source_code, path):
        if path.endswith('.py'):
            return self.py_skeletonizer.skeletonize(source_code, path)
        elif path.endswith(('.ts', '.tsx', '.js', '.jsx')):
            return self.ts_skeletonizer.skeletonize(source_code, path)
        elif path.endswith('.go'):
            return self.go_skeletonizer.skeletonize(source_code, path)
        else:
            # For non-supported files, treat content as the skeleton
            # Limit size to avoid DB bloat (e.g. 100KB)
            if len(source_code) > 100 * 1024:
                return f"# Content truncated (size: {len(source_code)} bytes)\n" + source_code[:100*1024] + "...", set()
            return source_code, set()
