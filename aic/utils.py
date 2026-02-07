import hashlib
import os
import fnmatch
import sys
import re

def calculate_hash(content):
    if isinstance(content, str):
        content = content.encode('utf-8')
    return hashlib.sha256(content).hexdigest()

def get_ignore_patterns(root_dir):
    """
    Loads ignore patterns from .geminiignore and .gitignore, plus defaults.
    """
    # Defaults
    patterns = {'.git', '.aic', '__pycache__', 'node_modules', '.DS_Store', 'venv', '.venv', 'env', '.env', 'dist', 'build'}
    
    for filename in ['.geminiignore', '.gitignore']:
        path = os.path.join(root_dir, filename)
        if os.path.exists(path):
            try:
                with open(path, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith('#'):
                            continue
                        # Normalize pattern: remove leading/trailing slashes for simple matching
                        # This is a naive implementation; proper gitignore handling is complex
                        clean_line = line.rstrip('/')
                        if clean_line:
                            patterns.add(clean_line)
            except Exception:
                pass # Fail silently on read errors
                
    return list(patterns)

def should_ignore(name, patterns):
    """
    Checks if a name matches any of the ignore patterns.
    """
    for pattern in patterns:
        if fnmatch.fnmatch(name, pattern):
            return True
    return False

def resolve_dep_to_path(dep_name, current_file, root_dir):
    """Refined heuristic to resolve module name to file path."""
    if not dep_name:
        return None

    # Ensure absolute paths for processing
    abs_root = os.path.abspath(root_dir)
    # current_file might be relative to root_dir
    abs_current_file = os.path.abspath(os.path.join(abs_root, current_file))
    curr_dir = os.path.dirname(abs_current_file)

    # Determine language from current_file
    ext = os.path.splitext(current_file)[1]
    
    # 1. Handle Relative Imports
    if dep_name.startswith('.'):
        levels = 0
        temp_dep = dep_name
        while temp_dep.startswith('.'):
            levels += 1
            temp_dep = temp_dep[1:]
        
        # .module (levels=1) -> same dir
        # ..module (levels=2) -> parent dir
        # ./ts (levels=1, temp_dep='/ts' or levels=2, temp_dep='ts'?) 
        # Actually:
        # ./ts starts with '.', levels=1, temp_dep='ts' if we handle it right.
        # But wait: './ts' -> starts with '.', one dot. Then '/ts'.
        # Let's be more robust:
        m = re.match(r'^(\.+)(.*)$', dep_name)
        dots = m.group(1)
        rel_path = m.group(2).lstrip('/\\').replace('.', os.sep)
        levels = len(dots)
        
        target_dir = curr_dir
        for _ in range(levels - 1):
            target_dir = os.path.dirname(target_dir)
        
        if len(target_dir) < len(abs_root):
            target_dir = abs_root
            
        base_path = os.path.join(target_dir, rel_path)
    else:
        # 2. Handle Absolute/Package Imports
        # Try resolving relative to root_dir
        base_path = os.path.join(abs_root, dep_name.replace('.', os.sep))

    # 3. Language specific candidates
    candidates = []
    if ext == '.py':
        candidates = [
            base_path + ".py",
            os.path.join(base_path, "__init__.py")
        ]
    elif ext in ('.ts', '.tsx', '.js', '.jsx'):
        candidates = [
            base_path + ".ts",
            base_path + ".tsx",
            base_path + ".js",
            base_path + ".jsx",
            os.path.join(base_path, "index.ts"),
            os.path.join(base_path, "index.js")
        ]
    elif ext == '.go':
        candidates = [
            base_path + ".go",
            os.path.join(base_path, "main.go")
        ]
        if os.path.isdir(base_path):
            try:
                for f in os.listdir(base_path):
                    if f.endswith('.go'):
                        candidates.append(os.path.join(base_path, f))
                        break
            except Exception:
                pass
    else:
        candidates = [base_path, base_path + ext]

    for cand in candidates:
        if os.path.exists(cand):
            return os.path.relpath(cand, abs_root)
            
    return None
