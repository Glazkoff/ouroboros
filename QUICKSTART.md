# Quick Start: Ouroboros with uv

## 🚀 One-Command Setup

```bash
cd /Users/glazkov/Development/ouroboros
./run.sh
```

This script will:
1. ✅ Check for uv (already installed on your system!)
2. ✅ Create virtual environment
3. ✅ Install dependencies with uv
4. ✅ Run GLM API test

## 📋 Manual Commands

### Test GLM API (Fastest)
```bash
cd /Users/glazkov/Development/ouroboros

# Option 1: Using existing venv
source .venv/bin/activate
python test_glm.py

# Option 2: One-liner with uv
uv run --with openai --with requests python test_glm.py
```

### Full Setup
```bash
# Create fresh venv with uv
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt

# Test
python test_glm.py

# Run local launcher
python local_launcher.py
```

## ⚡ Why uv?

| Tool | Speed | Notes |
|------|-------|-------|
| pip | 1x | Standard, slower |
| uv | 10-100x | Fast, Rust-based |

**Your system:** uv 0.6.8 is already installed! ✅

## 🎯 Current Status

✅ uv installed: `/Users/glazkov/.local/bin/uv`
✅ .env configured with GLM credentials
✅ Virtual environment: `.venv/`
✅ Dependencies: installed

⚠️ GLM API: Service overloaded (429), try again in 10-15 min

## 📝 Quick Reference

```bash
# Create venv
uv venv

# Install packages
uv pip install openai requests playwright playwright-stealth

# Install from requirements.txt
uv pip install -r requirements.txt

# Run script
python test_glm.py
python local_launcher.py
```

## 🐛 Troubleshooting

**GLM API 429 Error:**
- Service temporarily overloaded
- Wait 10-15 minutes
- Try again with: `python test_glm.py`

**Module not found:**
```bash
source .venv/bin/activate
uv pip install -r requirements.txt
```

**Playwright issues:**
```bash
uv pip install playwright
playwright install
```
