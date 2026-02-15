#!/usr/bin/env bash
#
# Conductor Marketplace Preparation Script
# Prepares Conductor for publication to multiple marketplaces
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

# Configuration
VERSION="0.2.0"
PROJECT_NAME="conductor"
REPO_URL="https://github.com/edithatogo/conductor-next"

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Calculate SHA256 checksum
calculate_checksum() {
    local file="$1"
    if command_exists sha256sum; then
        sha256sum "$file" | cut -d' ' -f1
    elif command_exists shasum; then
        shasum -a 256 "$file" | cut -d' ' -f1
    else
        log_error "No checksum tool found (sha256sum or shasum)"
        exit 1
    fi
}

# Prepare release artifacts
prepare_artifacts() {
    log_info "Preparing release artifacts..."

    # Create dist directory
    mkdir -p dist/

    # Create source distribution
    if [ -f "setup.cfg" ]; then
        log_info "Building Python package..."
        if command_exists python3; then
            python3 -m build --sdist --outdir dist/ 2>/dev/null || log_warning "Python build failed, skipping"
        fi
    fi

    # Create tarball of source
    log_info "Creating source tarball..."
    tar -czf "dist/${PROJECT_NAME}-${VERSION}.tar.gz" \
        --exclude=".git" \
        --exclude=".gitignore" \
        --exclude=".github" \
        --exclude="dist" \
        --exclude="*.egg-info" \
        --exclude=".pytest_cache" \
        --exclude="__pycache__" \
        --exclude=".coverage" \
        --exclude="*.pyc" \
        --exclude="*.pyo" \
        --exclude=".*.swp" \
        --exclude="TODO*" \
        -C . .

    log_success "Artifacts created in dist/"
}

# Update marketplace manifests with checksums
update_manifests() {
    log_info "Updating marketplace manifests with checksums..."

    local checksum=$(calculate_checksum "dist/${PROJECT_NAME}-${VERSION}.tar.gz")
    log_info "Calculated checksum: $checksum"

    # Update Homebrew formula
    if [ -f "HOMEBREW.md" ]; then
        sed -i.bak "s|TODO_REPLACE_WITH_ACTUAL_SHA256|$checksum|g" HOMEBREW.md
        log_success "Updated HOMEBREW.md with checksum"
    fi

    # Update Scoop manifest
    if [ -f "scoop/conductor.json" ]; then
        sed -i.bak "s|TODO_REPLACE_WITH_ACTUAL_HASH|$checksum|g" scoop/conductor.json
        log_success "Updated Scoop manifest with checksum"
    fi

    # Update package.json version
    if command_exists jq && [ -f "package.json" ]; then
        jq --arg v "$VERSION" '.version = $v' package.json > package.json.tmp && mv package.json.tmp package.json
        log_success "Updated package.json version to $VERSION"
    elif [ -f "package.json" ]; then
        sed -i.bak "s|\"version\": \".*\"|\"version\": \"$VERSION\"|g" package.json
        log_success "Updated package.json version to $VERSION"
    fi

    log_success "All manifests updated with correct checksums and versions"
}

# Verify marketplace readiness
verify_readiness() {
    log_info "Verifying marketplace readiness..."

    local ready_count=0
    local total_checks=0

    # Check mise integration
    ((total_checks++))
    if [ -f "mise.toml" ]; then
        log_success "✓ mise integration ready"
        ((ready_count++))
    else
        log_warning "✗ mise integration not found"
    fi

    # Check Smithery manifest
    ((total_checks++))
    if [ -f "smithery.toml" ]; then
        log_success "✓ Smithery manifest ready"
        ((ready_count++))
    else
        log_warning "✗ Smithery manifest not found"
    fi

    # Check PyPI setup
    ((total_checks++))
    if [ -f "setup.cfg" ] || [ -f "setup.py" ]; then
        log_success "✓ PyPI setup ready"
        ((ready_count++))
    else
        log_warning "✗ PyPI setup not found"
    fi

    # Check npm setup
    ((total_checks++))
    if [ -f "package.json" ]; then
        log_success "✓ npm setup ready"
        ((ready_count++))
    else
        log_warning "✗ npm setup not found"
    fi

    # Check Chocolatey setup
    ((total_checks++))
    if [ -f "chocolatey/conductor.nuspec" ]; then
        log_success "✓ Chocolatey setup ready"
        ((ready_count++))
    else
        log_warning "✗ Chocolatey setup not found"
    fi

    # Check Scoop setup
    ((total_checks++))
    if [ -f "scoop/conductor.json" ]; then
        log_success "✓ Scoop setup ready"
        ((ready_count++))
    else
        log_warning "✗ Scoop setup not found"
    fi

    log_info "Marketplace readiness: $ready_count/$total_checks checks passed"

    if [ $ready_count -eq $total_checks ]; then
        log_success "All marketplace integrations are ready for publication!"
    else
        log_warning "Some marketplace integrations need attention"
    fi
}

# Print publication instructions
print_publication_guide() {
    echo ""
    echo "========================================"
    echo "  Publication Guide"
    echo "========================================"
    echo ""
    echo "Artifacts prepared in dist/:"
    ls -la dist/ 2>/dev/null || echo "  (no artifacts yet)"
    echo ""
    echo "Ready for publication to:"
    echo "1. ${GREEN}Smithery${NC}: Run 'smithery publish' in project root"
    echo "2. ${GREEN}PyPI${NC}: Run 'twine upload dist/*'"
    echo "3. ${GREEN}npm${NC}: Run 'npm publish' in project root"
    echo "4. ${GREEN}Homebrew${NC}: Submit Formula/conductor.rb to homebrew-core"
    echo "5. ${GREEN}Chocolatey${NC}: Run 'choco pack && choco push *.nupkg'"
    echo "6. ${GREEN}Scoop${NC}: Add manifest to bucket and submit PR"
    echo ""
    echo "For detailed instructions, see MARKETPLACE_INTEGRATION.md"
    echo ""
}

# Main function
main() {
    echo ""
    echo "🚀 Conductor Marketplace Preparation"
    echo "====================================="
    echo ""

    prepare_artifacts
    update_manifests
    verify_readiness
    print_publication_guide

    log_success "Marketplace preparation complete!"
    echo ""
    echo "Next steps:"
    echo "1. Review dist/ artifacts"
    echo "2. Test installations in clean environments"
    echo "3. Follow publication instructions for desired marketplaces"
    echo "4. Update version numbers in all configs for next release"
}

main "$@"
