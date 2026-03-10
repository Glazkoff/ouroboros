#!/usr/bin/env python3
"""
Test GLM API integration.

Usage:
    python test_glm.py
"""

import os
import sys
from pathlib import Path

# Load .env file
def load_env():
    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, value = line.split("=", 1)
                    os.environ[key.strip()] = value.strip()
        print("✅ Loaded .env file")
    else:
        print("⚠️  No .env file found")

load_env()

# Test LLM client
from ouroboros.llm import LLMClient

def test_glm():
    print("\n" + "="*60)
    print("Testing GLM API Integration")
    print("="*60)

    # Create client
    client = LLMClient()
    print(f"\n📡 Provider: {client.provider}")
    print(f"🤖 Default model: {client.default_model()}")
    print(f"📋 Available models: {client.available_models()}")

    # Test simple chat
    print("\n" + "-"*60)
    print("Test 1: Simple chat")
    print("-"*60)

    messages = [
        {"role": "user", "content": "Hello! Please respond with a short greeting."}
    ]

    try:
        response, usage = client.chat(messages=messages, max_tokens=100)
        print(f"✅ Response: {response.get('content', 'No content')[:200]}")
        print(f"📊 Usage: {usage}")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

    # Test with tools
    print("\n" + "-"*60)
    print("Test 2: Chat with tools")
    print("-"*60)

    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get the current weather",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "City name"
                        }
                    },
                    "required": ["location"]
                }
            }
        }
    ]

    messages = [
        {"role": "user", "content": "What's the weather in Moscow?"}
    ]

    try:
        response, usage = client.chat(messages=messages, tools=tools, max_tokens=200)
        print(f"✅ Response: {response.get('content', 'No content')[:200]}")
        if response.get("tool_calls"):
            print(f"🔧 Tool calls: {response['tool_calls']}")
        print(f"📊 Usage: {usage}")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

    print("\n" + "="*60)
    print("✅ All tests passed!")
    print("="*60)
    return True

if __name__ == "__main__":
    success = test_glm()
    sys.exit(0 if success else 1)
