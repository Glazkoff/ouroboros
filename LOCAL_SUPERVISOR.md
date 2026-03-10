# Running Ouroboros Locally (Full Supervisor)

## 🚀 Quick Start

```bash
cd /Users/glazkov/Development/ouroboros

# Activate venv
source .venv/bin/activate

# Run local supervisor
python local_supervisor.py
```

## 📋 What Works

| Feature | Status | Notes |
|---------|--------|-------|
| GLM API | ✅ | Model: GLM-4.7 |
| OpenRouter | ✅ | Alternative provider |
| Telegram Polling | ✅ | No webhook needed |
| Direct Chat | ⚠️ | Basic integration |
| Worker Processes | ⚠️ | Limited in local mode |
| Self-Modification | ⚠️ | Manual git commits |
| Evolution Mode | ❌ | Requires Colab |
| Background Consciousness | ⚠️ | Experimental |

## 🎯 Commands

| Command | Description |
|---------|-------------|
| `/start` | Initialize bot |
| `/status` | Show status and budget |
| `/panic` | Emergency stop |
| `/restart` | Restart bot |
| `/bg` | Background consciousness status |

## 🔧 Configuration

Ensure `.env` has:

```bash
# LLM Provider
LLM_PROVIDER=glm
GLM_API_KEY=your_key
GLM_BASE_URL=https://api.z.ai/api/coding/paas/v4
GLM_MODEL=GLM-4.7

# Telegram
TELEGRAM_BOT_TOKEN=your_bot_token

# Budget
TOTAL_BUDGET=50

# GitHub (for self-modification)
GITHUB_TOKEN=your_token
GITHUB_USER=your_username
GITHUB_REPO=ouroboros
```

## 📝 Limitations

**Local mode is experimental.** For full functionality:

- **Evolution mode** → Use Colab
- **Background consciousness** → Limited
- **Worker processes** → Simplified
- **Git self-modification** → Manual commits

## 🐛 Troubleshooting

### "Module not found"
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### "Telegram API error"
- Check `TELEGRAM_BOT_TOKEN` in `.env`
- Verify bot with @BotFather

### "GLM API error"
- Check API key and balance
- Verify model: `GLM-4.7`

## 💡 For Full Functionality

Use Google Colab:
1. Upload `.env` to Colab Secrets
2. Run `colab_launcher.py`
3. Full evolution, consciousness, workers

See: [README.md](README.md) for Colab setup
