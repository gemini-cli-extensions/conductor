# Homebrew Tap for Conductor

## Installation

```bash
# Add the tap
brew tap edithatogo/conductor

# Install conductor
brew install conductor
```

## Creating the Formula

To create the Homebrew formula for Conductor, create a file named `conductor.rb` in the `Formula/` directory:

```ruby
class Conductor < Formula
  desc "Context-Driven Development tool for AI-assisted workflows"
  homepage "https://github.com/edithatogo/conductor-next"
  url "https://github.com/edithatogo/conductor-next/archive/v0.2.0.tar.gz"
  sha256 "TODO_REPLACE_WITH_ACTUAL_SHA256"
  license "MIT"

  depends_on "python@3.9"
  depends_on "node"
  depends_on "git"

  def install
    # Install core Python packages
    system "pip3", "install", *std_pip_args.add_test_deps.add_development_deps, buildpath

    # Install mise configuration
    (prefix/"etc/mise").install "mise.toml"

    # Install scripts
    bin.install Dir["scripts/*"]

    # Create launcher script
    (bin/"conductor").write <<~EOS
      #!/bin/bash
      exec mise run conductor "$@"
    EOS
  end

  test do
    system "#{bin}/conductor", "--version"
  end
end
```

## Publishing Process

1. Fork the [Homebrew/homebrew-core](https://github.com/Homebrew/homebrew-core) repository
2. Create the formula file in `Formula/conductor.rb`
3. Run `brew audit --new-formula conductor.rb` to check for issues
4. Submit a pull request with the formula

## Alternative: Personal Tap

For faster iteration, you can create a personal tap:

```bash
# Create your tap repository
mkdir -p ~/tap/edithatogo/conductor/Formula
cp conductor.rb ~/tap/edithatogo/conductor/Formula/
cd ~/tap/edithatogo/conductor
git init
git add .
git commit -m "Add conductor formula"
git remote add origin https://github.com/YOUR_USERNAME/homebrew-conductor.git
git push -u origin main

# Users can then install with:
brew tap edithatogo/conductor
brew install conductor
```
