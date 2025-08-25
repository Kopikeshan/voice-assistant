#!/usr/bin/env python3
"""
Quick test script to verify the voice assistant setup
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_setup():
    """Check if the voice assistant is properly set up."""
    print("🔍 Checking Voice Assistant Setup...")
    print("=" * 50)
    
    # Check for .env file
    if os.path.exists('.env'):
        print("✅ .env file found")
    else:
        print("⚠️  .env file not found - copy .env.example to .env")
    
    # Check for API keys
    groq_key = os.getenv('GROQ_API_KEY')
    hf_key = os.getenv('HUGGINGFACE_API_KEY')
    
    api_providers = []
    if groq_key and groq_key != 'your_groq_api_key_here':
        api_providers.append("Groq")
    if hf_key and hf_key != 'your_huggingface_token_here':
        api_providers.append("Hugging Face")
    
    # Check for Ollama
    try:
        import requests
        response = requests.get('http://localhost:11434/api/version', timeout=2)
        if response.status_code == 200:
            api_providers.append("Ollama (Local)")
    except:
        pass
    
    if api_providers:
        print(f"✅ AI Providers: {', '.join(api_providers)}")
    else:
        print("⚠️  No AI providers configured")
    
    # Check dependencies
    try:
        import speech_recognition
        print("✅ Speech recognition ready")
    except ImportError:
        print("❌ speech_recognition not installed")
    
    try:
        import pyttsx3
        print("✅ Text-to-speech ready")
    except ImportError:
        print("❌ pyttsx3 not installed")
    
    print("\n" + "=" * 50)
    if api_providers:
        print("🎉 Setup complete! Run: python voice_assistant.py")
    else:
        print("🔧 Please set up an AI provider in .env first")
        print("See README.md for instructions")

if __name__ == "__main__":
    check_setup()
