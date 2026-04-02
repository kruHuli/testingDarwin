#!/usr/bin/env python3
"""
Test which Claude models are available with your API key.
"""

import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

models_to_test = [
    "claude-3-5-sonnet-20241022",
    "claude-3-5-sonnet-20240620",
    "claude-3-sonnet-20240229",
    "claude-3-haiku-20240307",
    "claude-3-opus-20240229",
]

print("Testing which Claude models are available with your API key...\n")

for model in models_to_test:
    try:
        response = client.messages.create(
            model=model,
            max_tokens=10,
            messages=[{"role": "user", "content": "Hi"}]
        )
        print(f"✓ {model} - WORKS")
        print(f"  First working model found: {model}")
        print(f"\nUse this model for training!")
        break
    except Exception as e:
        error_msg = str(e)
        if "404" in error_msg or "not_found" in error_msg:
            print(f"✗ {model} - Not available")
        elif "401" in error_msg or "authentication" in error_msg.lower():
            print(f"✗ API key issue - check your .env file")
            break
        else:
            print(f"✗ {model} - Error: {error_msg[:100]}")
