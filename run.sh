#!/bin/bash
# Quick start script for Ouroboros with uv

set -e

echo "🚀 Ouroboros Quick Start (uv)"
echo "================================"
echo ""

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ uv not found. Installing..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    echo "✅ uv installed. Please restart your shell and run this script again."
    exit 1
fi

echo "✅ uv found: $(uv --version)"
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ No .env file found. Creating from .env.example..."
    cp .env.example .env
    echo "⚠️  Please edit .env with your credentials and run this script again."
    exit 1
fi

echo "✅ .env file found"
echo ""

# Create venv if not exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    uv venv
    echo "✅ Virtual environment created"
fi

# Activate venv
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies with uv..."
uv pip install -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Run test
echo "🧪 Running GLM API test..."
echo "================================"
python test_glm.py

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Test GLM API:     python test_glm.py"
echo "  2. Run local:        python local_launcher.py"
echo "  3. Or use Colab:     See README.md"
