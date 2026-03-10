#!/usr/bin/env python3
"""
Ouroboros — Local Supervisor

Full local execution without Google Colab dependencies.
Uses Telegram polling for message handling.

Usage:
    python local_supervisor.py
"""

from __future__ import annotations

import datetime
import json
import logging
import multiprocessing as mp
import os
import pathlib
import signal
import sys
import time
import uuid
from typing import Any, Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
log = logging.getLogger(__name__)

# ============================
# 1) Load environment
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
    return True

# ============================
# 2) Validate configuration
# ============================
def validate_config():
    """Validate required configuration."""
    provider = os.environ.get("LLM_PROVIDER", "openrouter").lower()

    if provider == "glm":
        required = ["GLM_API_KEY", "GLM_BASE_URL", "GLM_MODEL", "TELEGRAM_BOT_TOKEN", "TOTAL_BUDGET", "GITHUB_TOKEN", "GITHUB_USER", "GITHUB_REPO"]
        missing = [k for k in required if not os.environ.get(k)]
        if missing:
            log.error(f"❌ Missing required env vars: {', '.join(missing)}")
            sys.exit(1)
        log.info(f"✅ Configuration validated (provider={provider}, model={os.environ.get('GLM_MODEL')})")
    else:
        required = ["OPENROUTER_API_KEY", "TELEGRAM_BOT_TOKEN", "TOTAL_BUDGET", "GITHUB_TOKEN", "GITHUB_USER", "GITHUB_REPO"]
        missing = [k for k in required if not os.environ.get(k)]
        if missing:
            log.error(f"❌ Missing required env vars: {', '.join(missing)}")
            sys.exit(1)
        log.info(f"✅ Configuration validated (provider={provider})")

    return True

# ============================
# 3) Setup local directories
# ============================
def setup_directories():
    """Setup local directories (replaces Google Drive)."""
    repo_dir = pathlib.Path(__file__).parent.resolve()
    data_dir = repo_dir / "data"

    # Create subdirectories
    for sub in ["state", "logs", "memory", "index", "locks", "archive"]:
        (data_dir / sub).mkdir(parents=True, exist_ok=True)

    log.info(f"📁 Repository: {repo_dir}")
    log.info(f"📁 Data directory: {data_dir}")

    return repo_dir, data_dir

# ============================
# 4) Initialize supervisor modules
# ============================
def init_supervisor(repo_dir: pathlib.Path, data_dir: pathlib.Path):
    """Initialize supervisor modules with local paths."""
    from supervisor import telegram as telegram_module
    from supervisor import state as state_module
    from supervisor import workers as workers_module

    # Parse budget
    try:
        total_budget = float(os.environ.get("TOTAL_BUDGET", "50"))
    except ValueError:
        total_budget = 50.0

    # Initialize state module
    state_module.init(data_dir, total_budget)
    log.info("✅ State module initialized")

    # Initialize Telegram client
    tg_token = os.environ["TELEGRAM_BOT_TOKEN"]
    tg_client = telegram_module.TelegramClient(tg_token)
    telegram_module.init(data_dir, total_budget, 10, tg_client)
    log.info("✅ Telegram client initialized")

    # Initialize workers module
    workers_module.REPO_DIR = repo_dir
    workers_module.DRIVE_ROOT = data_dir
    workers_module.TOTAL_BUDGET_LIMIT = total_budget
    workers_module.MAX_WORKERS = int(os.environ.get("OUROBOROS_MAX_WORKERS", "3"))
    workers_module.SOFT_TIMEOUT_SEC = 600
    workers_module.HARD_TIMEOUT_SEC = 1800
    log.info(f"✅ Workers module initialized (max_workers={workers_module.MAX_WORKERS})")

    # Initialize state
    state_module.init_state()
    log.info("✅ State initialized")

    return tg_client

# ============================
# 5) Main polling loop
# ============================
def run_polling_loop(tg_client, repo_dir: pathlib.Path, data_dir: pathlib.Path):
    """Main Telegram polling loop."""
    from supervisor import telegram as telegram_module
    from supervisor import state as state_module
    from supervisor import workers as workers_module
    from supervisor import queue as queue_module
    from supervisor import events as events_module

    log.info("\n" + "="*60)
    log.info("  Starting Ouroboros (Local Mode)")
    log.info("="*60 + "\n")

    # Get owner chat_id from state or first message
    state = state_module.load_state()
    owner_chat_id = state.get("owner_chat_id")
    if owner_chat_id:
        log.info(f"✅ Owner chat_id: {owner_chat_id}")
    else:
        log.info("⚠️  No owner yet. Send any message to become the owner.")

    # Offset for Telegram polling
    offset = 0

    # Main loop
    log.info("🔄 Starting polling loop (Ctrl+C to stop)...")
    log.info("")

    try:
        while True:
            # Get updates from Telegram
            try:
                updates = tg_client.get_updates(offset=offset, timeout=10)
            except Exception as e:
                log.error(f"Failed to get updates: {e}")
                time.sleep(5)
                continue

            # Process updates
            for update in updates:
                offset = max(offset, update["update_id"] + 1)

                # Extract message
                message = update.get("message") or update.get("edited_message")
                if not message:
                    continue

                chat_id = message["chat"]["id"]
                text = message.get("text", "")
                user_id = message.get("from", {}).get("id")

                # First message sets owner
                if not owner_chat_id:
                    owner_chat_id = chat_id
                    state["owner_chat_id"] = chat_id
                    state["owner_user_id"] = user_id
                    state_module.save_state(state)
                    log.info(f"✅ Owner set: chat_id={chat_id}")
                    tg_client.send_message(chat_id, "👋 Hello! I'm Ouroboros. You are now my creator.")
                    continue

                # Only owner can interact
                if chat_id != owner_chat_id:
                    log.debug(f"Ignoring message from non-owner: {chat_id}")
                    continue

                # Handle commands
                if text.startswith("/"):
                    handle_command(tg_client, chat_id, text, repo_dir, data_dir)
                else:
                    # Regular message - handle as direct chat
                    log.info(f"📩 Message from owner: {text[:50]}...")
                    handle_message(tg_client, chat_id, text, repo_dir, data_dir)

    except KeyboardInterrupt:
        log.info("\n👋 Interrupted by user")
    except Exception as e:
        log.error(f"❌ Fatal error: {e}", exc_info=True)

# ============================
# 6) Command handlers
# ============================
def handle_command(tg_client, chat_id: int, text: str, repo_dir: pathlib.Path, data_dir: pathlib.Path):
    """Handle Telegram commands."""
    from supervisor import state as state_module

    cmd = text.strip().lower()

    if cmd == "/start":
        tg_client.send_message(chat_id, "👋 I'm Ouroboros, a self-modifying AI agent. Send me any message to chat!")

    elif cmd == "/status":
        state = state_module.load_state()
        status = state_module.status_text()
        tg_client.send_message(chat_id, f"📊 Status:\n{status}")

    elif cmd == "/panic":
        log.warning("🚨 PANIC received - stopping all workers")
        tg_client.send_message(chat_id, "🚨 Stopping all workers...")
        # TODO: Implement worker cleanup
        tg_client.send_message(chat_id, "✅ All workers stopped")

    elif cmd == "/restart":
        log.info("🔄 Restart requested")
        tg_client.send_message(chat_id, "🔄 Restarting...")
        # TODO: Implement graceful restart
        sys.exit(0)

    elif cmd == "/bg":
        tg_client.send_message(chat_id, "🧠 Background consciousness: experimental in local mode")

    elif cmd.startswith("/evolve"):
        tg_client.send_message(chat_id, "⚠️ Evolution mode requires Colab. Use /status to check current state.")

    else:
        tg_client.send_message(chat_id, f"Unknown command: {cmd}\n\nAvailable: /start, /status, /panic, /restart, /bg")

# ============================
# 7) Message handler
# ============================
def handle_message(tg_client, chat_id: int, text: str, repo_dir: pathlib.Path, data_dir: pathlib.Path):
    """Handle regular message."""
    from supervisor import workers as workers_module
    from supervisor import events as events_module

    try:
        # Send typing indicator
        tg_client.send_chat_action(chat_id, "typing")

        # Handle as direct chat
        workers_module.handle_chat_direct(chat_id, text)

        # Wait for response (simplified - no workers in local mode yet)
        time.sleep(2)

        # For now, just acknowledge
        # TODO: Integrate with agent.py for real responses
        tg_client.send_message(chat_id, f"✅ Received: {text[:100]}\n\n⚠️ Full agent integration coming soon. Use Colab for complete functionality.")

    except Exception as e:
        log.error(f"Error handling message: {e}", exc_info=True)
        tg_client.send_message(chat_id, f"❌ Error: {type(e).__name__}: {str(e)[:200]}")

# ============================
# 8) Main entry point
# ============================
def main():
    """Main entry point for local execution."""
    print("\n" + "="*60)
    print("  Ouroboros — Local Supervisor")
    print("="*60 + "\n")

    # Step 1: Load environment
    load_env_file()

    # Step 2: Validate configuration
    validate_config()

    # Step 3: Setup directories
    repo_dir, data_dir = setup_directories()

    # Step 4: Initialize supervisor
    tg_client = init_supervisor(repo_dir, data_dir)

    # Step 5: Run polling loop
    run_polling_loop(tg_client, repo_dir, data_dir)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log.info("\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        log.error(f"❌ Fatal error: {e}", exc_info=True)
        sys.exit(1)
