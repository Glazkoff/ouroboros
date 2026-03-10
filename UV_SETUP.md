# Running Ouroboros with uv

[uv](https://github.com/astral-sh/uv) is a fast Python package installer and resolver. Here's how to use it with Ouroboros.

## Quick Start

### Option 1: One-liner (Fastest)

```bash
cd /Users/glazkov/Development/ouroboros

# Test GLM API
uv run --with openai --with requests python test_glm.py

# Run local launcher
uv run --with openai --with requests --with playwright --with playwright-stealth python local_launcher.py
```

### Option 2: Create Virtual Environment

```bash
cd /Users/glazkov/Development/ouroboros

# Create venv with uv
uv venv

# Activate
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv pip install -r requirements.txt

# Run
python test_glm.py
python local_launcher.py
```

### Option 3: Sync from pyproject.toml

```bash
cd /Users/glazkov/Development/ouroboros

# Sync dependencies
uv sync

# Run
uv run python test_glm.py
```

## Complete Setup with uv

```bash
# 1. Clone your fork
git clone https://github.com/Glazkoff/ouroboros.git
cd ouroboros

# 2. Configure
cp .env.example .env
# Edit .env with your credentials

# 3. Create environment and install deps
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt

# 4. Test GLM API
uv run python test_glm.py

# 5. Run local launcher
uv run python local_launcher.py
```

## Benefits of uv

- ⚡ **10-100x faster** than pip
- 🔒 **Deterministic** dependency resolution
- 🎯 **Automatic Python version management**
- 📦 **Single binary** installation

## Install uv

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or via Homebrew
brew install uv

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## Troubleshooting

### "uv: command not found"
Install uv first (see above).

### Dependency conflicts
```bash
# Clean install
rm -rf .venv
uv venv
uv pip install -r requirements.txt
```

### Playwright not working
```bash
uv pip install playwright
playwright install
```

## Full Command Reference

```bash
# Create venv
uv venv

# Install packages
uv pip install openai requests playwright playwright-stealth

# Install from requirements.txt
uv pip install -r requirements.txt

# Run script with dependencies
uv run --with openai --with requests python script.py

# Run in existing venv
source .venv/bin/activate
python script.py
```
