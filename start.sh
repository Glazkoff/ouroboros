#!/bin/bash
# Restart local supervisor with the fix

set -e

echo "🔄 Restarting Ouroboros Local Supervisor..."
echo ""

cd /Users/glazkov/Development/ouroboros

# Pull latest changes
echo "📦 Pulling latest changes..."
git pull origin main

# Activate venv
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Run
echo "🚀 Starting supervisor..."
echo ""
python local_supervisor.py
