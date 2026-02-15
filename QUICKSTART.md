# Quick Start Guide

Get up and running with Conductor in minutes using one of our installation methods.

## One-Click Installation (Recommended)

The fastest way to install Conductor is using our universal installer:

### Unix/macOS

```bash
curl -fsSL install.cat/edithatogo/conductor-next | sh
```

### Windows (PowerShell)

```powershell
irm install.cat/edithatogo/conductor-next | iex
```

This installer uses [mise](https://mise.jdx.dev/) to manage dependencies and provides the most consistent experience across platforms.

## Alternative Installation Methods

### Via mise directly

```bash
mise install edithatogo/conductor-next
```

### Via Smithery (Coming Soon)

```bash
smithery install conductor
```

### Manual Installation

If you prefer to install manually:

1. Clone the repository:

   ```bash
   git clone https://github.com/edithatogo/conductor-next.git
   cd conductor-next
   ```

2. Install dependencies using mise:

   ```bash
   mise install
   ```

3. Run the installer:

   ```bash
   python scripts/conductor_install.py --all
   ```

## Verify Installation

After installation, verify everything is working:

```bash
# Check if mise is working
mise --version

# Verify Conductor components
python -c "import conductor_core; print('Core installed')"
```

## Next Steps

Once installed, initialize your project:

```bash
/conductor:setup
```

Then create your first track:

```bash
/conductor:newTrack "My first feature"
```

## Troubleshooting

If you encounter issues:

1. **Check prerequisites**: Ensure Git, Python 3.9+, and Node.js 18+ are installed
2. **Verify mise**: Run `mise doctor` to diagnose issues
3. **Check PATH**: Ensure mise and Conductor binaries are in your PATH
4. **Review logs**: Check the installer output for specific error messages

For more detailed troubleshooting, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md).
