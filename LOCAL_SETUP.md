# Running Ouroboros Locally

Ouroboros is designed for Google Colab, but you can run it locally with some modifications.

## Quick Start (Recommended: Colab)

For full functionality, use Google Colab:
1. See [README.md](README.md) for Colab setup instructions
2. Colab provides: free GPU, persistent storage via Google Drive, easy secret management

## Local Setup (Experimental)

### Prerequisites

- Python 3.10+
- Git
- Telegram bot token (from @BotFather)
- GitHub personal access token

### Step 1: Clone and Configure

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/ouroboros.git
cd ouroboros

# Create .env file
cp .env.example .env
# Edit .env with your credentials
```

### Step 2: Install Dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Step 3: Test GLM API (if using GLM)

```bash
python test_glm.py
```

### Step 4: Run (Limited Functionality)

```bash
python local_launcher.py
```

**Note:** Local execution has limitations:
- No automatic git self-modification (needs manual setup)
- No Google Drive persistence
- Supervisor loop not fully implemented
- For full functionality, use Colab

## Full Local Setup (Advanced)

For complete local functionality, you need to:

1. **Modify `colab_launcher.py`**:
   - Remove `google.colab` imports
   - Replace Drive storage with local filesystem
   - Setup environment variables

2. **Implement local supervisor**:
   - Worker lifecycle management
   - Telegram bot polling (not webhook)
   - State persistence

3. **Configure git**:
   ```bash
   git config user.name "Ouroboros"
   git config user.email "ouroboros@local"
   ```

4. **Run**:
   ```bash
   python colab_launcher.py  # with modifications
   ```

## Docker (Alternative)

Create a `Dockerfile` for isolated local execution:

```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "local_launcher.py"]
```

Build and run:
```bash
docker build -t ouroboros .
docker run --env-file .env ouroboros
```

## Troubleshooting

### "No module named 'google.colab'"
- This is expected when running locally
- Use `local_launcher.py` instead of `colab_launcher.py`

### GLM API errors
- Check your API key and balance
- Verify model name: `GLM-4.7`
- See test script: `python test_glm.py`

### Telegram bot not responding
- Verify `TELEGRAM_BOT_TOKEN` in `.env`
- Check bot status with @BotFather

## Need Help?

- Full Colab setup: [README.md](README.md)
- Issues: [GitHub Issues](https://github.com/YOUR_USERNAME/ouroboros/issues)
- Original repo: [joi-lab/ouroboros](https://github.com/joi-lab/ouroboros)
