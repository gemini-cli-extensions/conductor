import argparse
import os
from aic.db import init_db, upsert_node, get_node, get_dependencies, update_edges, mark_dirty
from aic.skeleton import RichSkeletonizer
from aic.utils import calculate_hash

def index_repo(root_dir="."):
    init_db()
    skeletonizer = RichSkeletonizer()
    for root, dirs, files in os.walk(root_dir):
        # Exclusions
        dirs[:] = [d for d in dirs if d not in ('.git', '.aic', '__pycache__', 'node_modules')]
        
        for file in files:
            if not file.endswith('.py'):
                continue
                
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, root_dir)
            
            with open(file_path, 'r') as f:
                content = f.read()
                
            current_hash = calculate_hash(content)
            existing = get_node(rel_path)
            
            if existing and existing['hash'] == current_hash:
                continue
                
            print(f"Indexing: {rel_path}")
            skeleton, dependencies = skeletonizer.skeletonize(content, rel_path)
            upsert_node(rel_path, current_hash, skeleton)
            mark_dirty(rel_path)
            
            # Resolve dependencies to file paths
            resolved_deps = []
            for dep in dependencies:
                resolved = resolve_dep_to_path(dep, rel_path, root_dir)
                if resolved:
                    resolved_deps.append(resolved)
            
            update_edges(rel_path, resolved_deps)

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

def get_context(file_path):
    node = get_node(file_path)
    if not node:
        return f"# Error: {file_path} not indexed."
    
    output = [f"# Context for {file_path}", node['skeleton'], ""]
    
    deps = get_dependencies(file_path)
    if deps:
        output.append("## Dependencies")
        for dep in deps:
            dep_node = get_node(dep)
            if dep_node:
                output.append(f"### {dep}")
                output.append(dep_node['skeleton'])
                output.append("")
    
    return "\n".join(output)

def main():
    parser = argparse.ArgumentParser(description="AIC: AI Compiler")
    subparsers = parser.add_subparsers(dest="command")
    
    subparsers.add_parser("index")
    
    context_parser = subparsers.add_parser("context")
    context_parser.add_argument("file")
    
    args = parser.parse_args()
    
    if args.command == "index":
        index_repo()
        print("Finished indexing.")
    elif args.command == "context":
        print(get_context(args.file))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
