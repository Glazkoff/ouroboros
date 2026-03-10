#!/usr/bin/env python3
"""
Ouroboros — Local launcher (alternative to colab_launcher.py)

Run Ouroboros locally without Google Colab.

Usage:
    python local_launcher.py

Requirements:
    - Python 3.10+
    - .env file with configuration
    - Telegram bot token
"""

import logging
import os
import sys
import time
import pathlib
import subprocess
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
log = logging.getLogger(__name__)

# ============================
# 1) Load .env file
# ============================
def load_env_file():
    """Load environment variables from .env file."""
    env_file = pathlib.Path(__file__).parent / ".env"
    if not env_file.exists():
        log.error("❌ No .env file found. Please create one from .env.example")
        sys.exit(1)

    log.info(f"📁 Loading .env from {env_file}")
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()
                # Remove quotes if present
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                elif value.startswith("'") and value.endswith("'"):
                    value = value[1:-1]
                os.environ[key] = value

    log.info("✅ Environment variables loaded")

# ============================
# 2) Install dependencies
# ============================
def install_deps():
    """Install required dependencies."""
    log.info("📦 Installing dependencies...")
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-q", "-r", "requirements.txt"],
        check=True,
    )
    log.info("✅ Dependencies installed")

# ============================
# 3) Validate configuration
# ============================
def validate_config():
    """Validate required configuration."""
    provider = os.environ.get("LLM_PROVIDER", "openrouter").lower()

    if provider == "glm":
        required = ["GLM_API_KEY", "GLM_BASE_URL", "GLM_MODEL", "TELEGRAM_BOT_TOKEN", "TOTAL_BUDGET", "GITHUB_TOKEN"]
        missing = [k for k in required if not os.environ.get(k)]
        if missing:
            log.error(f"❌ Missing required env vars: {', '.join(missing)}")
            log.error("Please check your .env file")
            sys.exit(1)
        log.info(f"✅ Configuration validated (provider={provider}, model={os.environ.get('GLM_MODEL')})")
    else:
        required = ["OPENROUTER_API_KEY", "TELEGRAM_BOT_TOKEN", "TOTAL_BUDGET", "GITHUB_TOKEN"]
        missing = [k for k in required if not os.environ.get(k)]
        if missing:
            log.error(f"❌ Missing required env vars: {', '.join(missing)}")
            log.error("Please check your .env file")
            sys.exit(1)
        log.info(f"✅ Configuration validated (provider={provider})")

# ============================
# 4) Setup local directories
# ============================
def setup_directories():
    """Setup local directories (replaces Google Drive)."""
    repo_dir = pathlib.Path(__file__).parent
    data_dir = repo_dir / "data"
    data_dir.mkdir(exist_ok=True)

    # Set environment variables for supervisor
    os.environ["OUROBOROS_REPO_DIR"] = str(repo_dir)
    os.environ["OUROBOROS_DATA_DIR"] = str(data_dir)

    log.info(f"📁 Repository: {repo_dir}")
    log.info(f"📁 Data directory: {data_dir}")

    return repo_dir, data_dir

# ============================
# 5) Main entry point
# ============================
def main():
    """Main entry point for local execution."""
    print("\n" + "="*60)
    print("  Ouroboros — Local Launcher")
    print("="*60 + "\n")

    # Step 1: Load environment
    load_env_file()

    # Step 2: Install dependencies
    install_deps()

    # Step 3: Validate configuration
    validate_config()

    # Step 4: Setup directories
    repo_dir, data_dir = setup_directories()

    # Step 5: Import and run supervisor
    log.info("\n" + "="*60)
    log.info("  Starting Ouroboros...")
    log.info("="*60 + "\n")

    # Monkey-patch supervisor config for local execution
    import supervisor.workers as workers
    import supervisor.state as state

    # Override paths
    workers.REPO_DIR = repo_dir
    workers.DRIVE_ROOT = data_dir
    state.STATE_FILE = data_dir / "state.json"
    state.EVENTS_FILE = data_dir / "events.jsonl"

    # Import colab_launcher's main loop
    # Note: colab_launcher.py has Colab-specific imports, so we can't import it directly
    # Instead, we'll create a minimal supervisor loop here

    log.warning("⚠️  Local execution is experimental")
    log.warning("⚠️  For full functionality, use Google Colab")
    log.warning("⚠️  See: colab_launcher.py for reference\n")

    # TODO: Implement local supervisor loop
    # For now, just run a simple test
    log.info("Running GLM API test...")
    subprocess.run([sys.executable, "test_glm.py"], check=False)

    log.info("\n✅ Local setup complete!")
    log.info("📝 To fully run Ouroboros locally, you need to:")
    log.info("   1. Implement local supervisor loop (replace colab_launcher.py)")
    log.info("   2. Setup Telegram bot webhook or polling")
    log.info("   3. Configure git for self-modification")
    log.info("\n💡 Or use Google Colab for full functionality")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log.info("\n👋 Interrupted by user")
        sys.exit(0)
    except Exception as e:
        log.error(f"❌ Error: {e}", exc_info=True)
        sys.exit(1)
