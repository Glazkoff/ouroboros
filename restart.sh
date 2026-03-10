#!/bin/bash
# Quick restart script for Ouroboros

echo "🔄 Restarting Ouroboros..."
echo ""

cd /Users/glazkov/Development/ouroboros

# Pull latest changes
echo "📦 Pulling changes..."
git pull origin ouroboros 2>/dev/null || git pull origin main

# Activate venv
echo "🔧 Activating environment..."
source .venv/bin/activate

# Start
echo "🚀 Starting Ouroboros..."
echo ""
python local_supervisor.py
