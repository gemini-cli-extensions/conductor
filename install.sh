#!/usr/bin/env bash
#
# Conductor Universal Installer for Unix/macOS
# One-liner install: curl -fsSL install.cat/edithatogo/conductor-next | sh
#

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
REPO_URL="https://github.com/edithatogo/conductor-next.git"
INSTALL_DIR="${HOME}/.local/share/conductor-next"
CONDUCTOR_VERSION="0.2.0"

# Logging functions
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

# Detect OS
detect_os() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux"
    else
        echo "unknown"
    fi
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Install mise if not present
install_mise() {
    if command_exists mise; then
        log_info "mise is already installed"
        return 0
    fi

    log_info "Installing mise..."

    if command_exists curl; then
        curl https://mise.run | sh
    elif command_exists wget; then
        wget -qO- https://mise.run | sh
    else
        log_error "Neither curl nor wget found. Please install one of them first."
        exit 1
    fi

    # Add mise to PATH for current session
    export PATH="$HOME/.local/bin:$PATH"

    if ! command_exists mise; then
        log_error "mise installation failed"
        exit 1
    fi

    log_success "mise installed successfully"
}

# Clone or update repository
clone_repository() {
    log_info "Setting up conductor-next repository..."

    if [ -d "$INSTALL_DIR" ]; then
        log_info "Repository already exists at $INSTALL_DIR, updating..."
        cd "$INSTALL_DIR"
        git pull origin main || git pull origin master || true
    else
        log_info "Cloning repository to $INSTALL_DIR..."
        mkdir -p "$(dirname "$INSTALL_DIR")"
        git clone --depth 1 "$REPO_URL" "$INSTALL_DIR"
        cd "$INSTALL_DIR"
    fi

    log_success "Repository ready at $INSTALL_DIR"
}

# Setup mise environment
setup_mise() {
    log_info "Setting up mise environment..."

    # Install tools defined in mise.toml
    mise install

    log_success "mise environment ready"
}

# Install all components
install_components() {
    log_info "Installing conductor components..."

    # Run the Python installer
    if [ -f "scripts/conductor_install.py" ]; then
        python3 scripts/conductor_install.py --all
    else
        log_warning "conductor_install.py not found, using mise tasks..."
        mise run install-all
    fi

    log_success "Components installed"
}

# Setup shell integration
setup_shell() {
    log_info "Setting up shell integration..."

    local shell_rc=""

    if [ -n "$ZSH_VERSION" ]; then
        shell_rc="$HOME/.zshrc"
    elif [ -n "$BASH_VERSION" ]; then
        shell_rc="$HOME/.bashrc"
    else
        log_warning "Unknown shell, skipping shell integration"
        return 0
    fi

    # Add mise activation if not already present
    if ! grep -q "mise activate" "$shell_rc" 2>/dev/null; then
        echo "" >> "$shell_rc"
        echo "# Conductor-next (mise)" >> "$shell_rc"
        echo 'eval "$("$HOME/.local/bin/mise" activate)' >> "$shell_rc"
        log_success "Added mise activation to $shell_rc"
    fi

    # Add conductor to PATH if not already present
    if ! grep -q "$INSTALL_DIR" "$shell_rc" 2>/dev/null; then
        echo "export PATH=\"$INSTALL_DIR/scripts:\$PATH\"" >> "$shell_rc"
        log_success "Added conductor scripts to PATH"
    fi
}

# Print installation summary
print_summary() {
    echo ""
    echo "========================================"
    echo "  Installation Complete!"
    echo "========================================"
    echo ""
    echo -e "${GREEN}✓${NC} mise installed and configured"
    echo -e "${GREEN}✓${NC} conductor-next cloned to $INSTALL_DIR"
    echo -e "${GREEN}✓${NC} All components installed"
    echo ""
    echo "Next steps:"
    echo "  1. Restart your terminal or run: source ~/.bashrc (or ~/.zshrc)"
    echo "  2. Run 'mise doctor' to verify installation"
    echo "  3. Run 'mise run verify' to verify conductor components"
    echo ""
    echo "Useful commands:"
    echo "  mise run sync-upstream    # Sync with upstream repos"
    echo "  mise run update-all       # Check for updates"
    echo "  mise run verify           # Verify installation"
    echo ""
    echo "Documentation:"
    echo "  $INSTALL_DIR/README.md"
    echo ""
    log_success "Enjoy using conductor-next!"
}

# Main installation flow
main() {
    echo ""
    echo "🚀 Conductor Universal Installer"
    echo "========================================"
    echo ""

    local os=$(detect_os)
    log_info "Detected OS: $os"

    # Check prerequisites
    if ! command_exists git; then
        log_error "git is required but not installed"
        exit 1
    fi

    # Run installation steps
    install_mise
    clone_repository
    setup_mise
    install_components
    setup_shell

    # Print summary
    print_summary
}

# Run main function
main "$@"
