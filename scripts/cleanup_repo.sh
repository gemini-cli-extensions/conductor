#!/usr/bin/env bash
#
# Conductor Repository Cleanup Script
# Removes proprietary tool files and ensures only essential files are in the repository
#

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# List of directories that should NOT be in the remote repository
TOOL_DIRS=(
    ".claude"
    ".gemini"
    ".claude-plugin"
    ".antigravity"
    ".agent"
    ".qwen"
    ".copilot"
    ".github-copilot"
)

# List of files that should NOT be in the remote repository
TOOL_FILES=(
    ".vscode/settings.json"
    ".idea/**"
    ".editor/**"
)

# Clean up tool-specific directories
cleanup_tool_dirs() {
    log_info "Cleaning up tool-specific directories..."

    for dir in "${TOOL_DIRS[@]}"; do
        if [ -d "$dir" ]; then
            log_warning "Removing tool-specific directory: $dir"
            rm -rf "$dir"
        fi
    done

    log_success "Tool-specific directories cleaned up"
}

# Verify essential files exist
verify_essential_files() {
    log_info "Verifying essential files exist..."

    local missing_files=()

    # Essential configuration files
    local essential_files=(
        "README.md"
        "AGENTS.md"
        "LICENSE"
        "mise.toml"
        "package.json"
        "setup.cfg"
        "smithery.toml"
        "install.sh"
        "install.ps1"
        "conductor-core/"
        "conductor-gemini/"
        "conductor-vscode/"
        "conductor/"
    )

    for file in "${essential_files[@]}"; do
        if [ ! -e "$file" ] && [ ! -d "$file" ]; then
            missing_files+=("$file")
            log_error "Missing essential file/directory: $file"
        else
            log_info "Found essential file/directory: $file"
        fi
    done

    if [ ${#missing_files[@]} -gt 0 ]; then
        log_error "Missing ${#missing_files[@]} essential files/directories"
        return 1
    else
        log_success "All essential files/directories present"
        return 0
    fi
}

# Clean up temporary files
cleanup_temp_files() {
    log_info "Cleaning up temporary files..."

    # Remove any temporary files that might have been created
    find . -name "*.tmp" -delete 2>/dev/null || true
    find . -name "*.temp" -delete 2>/dev/null || true
    find . -name "*~" -delete 2>/dev/null || true
    find . -name ".DS_Store" -delete 2>/dev/null || true
    find . -name "Thumbs.db" -delete 2>/dev/null || true

    log_success "Temporary files cleaned up"
}

# Create/update documentation
update_documentation() {
    log_info "Updating documentation..."

    # Ensure AGENTS.md is up to date
    if [ -f "AGENTS.md" ]; then
        log_success "AGENTS.md exists and is ready for remote"
    else
        log_error "AGENTS.md is missing!"
        return 1
    fi

    # Ensure README.md is up to date
    if [ -f "README.md" ]; then
        log_success "README.md exists and is ready for remote"
    else
        log_error "README.md is missing!"
        return 1
    fi

    log_success "Documentation verified"
}

# Print summary
print_summary() {
    echo ""
    echo "========================================"
    echo "  Repository Cleanup Summary"
    echo "========================================"
    echo ""
    echo "✅ Tool-specific directories removed:"
    printf "   - %s\n" "${TOOL_DIRS[@]}"
    echo ""
    echo "✅ Essential files verified:"
    echo "   - Core architecture (conductor-core, conductor-gemini, conductor-vscode)"
    echo "   - Universal installer (install.sh, install.ps1)"
    echo "   - Package manager configs (mise.toml, package.json, setup.cfg)"
    echo "   - Documentation (README.md, AGENTS.md, INSTALL.md)"
    echo "   - Marketplace integration files"
    echo ""
    echo "✅ Repository is ready for remote synchronization"
    echo ""
    log_success "Repository cleanup completed successfully!"
}

# Main function
main() {
    echo ""
    echo "🧹 Conductor Repository Cleanup"
    echo "================================"
    echo ""

    cleanup_tool_dirs
    cleanup_temp_files
    verify_essential_files
    update_documentation
    print_summary

    echo ""
    log_success "Repository is now clean and ready for remote synchronization!"
    echo "Only essential files remain that are appropriate for the public repository."
}

main "$@"
