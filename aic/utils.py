import hashlib
import os
import fnmatch

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
    """Simple heuristic to resolve module name to file path."""
    # Handle relative imports (e.g., '.module' or '..module')
    if dep_name.startswith('.'):
        levels = 0
        while dep_name.startswith('.'):
            levels += 1
            dep_name = dep_name[1:]
        
        curr_dir = os.path.dirname(current_file)
        for _ in range(levels - 1):
            curr_dir = os.path.dirname(curr_dir)
        
        base_path = os.path.join(curr_dir, dep_name.replace('.', os.sep))
    else:
        base_path = os.path.join(root_dir, dep_name.replace('.', os.sep))

    candidates = [
        base_path + ".py",
        os.path.join(base_path, "__init__.py")
    ]
    
    for cand in candidates:
        if os.path.exists(cand):
            return os.path.relpath(cand, root_dir)
    return None
