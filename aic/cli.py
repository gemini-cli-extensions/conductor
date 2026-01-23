import argparse
import os
from aic.db import init_db, upsert_node, get_node, get_dependencies, update_edges, mark_dirty
from aic.skeleton import UniversalSkeletonizer
from aic.utils import calculate_hash, resolve_dep_to_path, get_ignore_patterns, should_ignore

def index_repo(root_dir="."):
    init_db()
    skeletonizer = UniversalSkeletonizer()
    ignore_patterns = get_ignore_patterns(root_dir)
    
    indexed_count = 0
    
    for root, dirs, files in os.walk(root_dir):
        # Exclusions
        dirs[:] = [d for d in dirs if not should_ignore(d, ignore_patterns)]
        
        for file in files:
            if should_ignore(file, ignore_patterns):
                continue
                
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, root_dir)
            
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
            indexed_count += 1
            
    print(f"Finished indexing. Processed {indexed_count} files.")

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
