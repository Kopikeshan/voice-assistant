#!/usr/bin/env python3
"""
Free AI Providers Setup Script
Helps you set up free AI providers for your voice assistant.
"""

import os
import sys
import requests

def check_ollama():
    """Check if Ollama is running locally."""
    try:
        response = requests.get('http://localhost:11434/api/version', timeout=2)
        if response.status_code == 200:
            version_info = response.json()
            print("✅ Ollama is running locally!")
            print(f"   Version: {version_info.get('version', 'Unknown')}")
            
            # Check available models
            try:
                models_response = requests.get('http://localhost:11434/api/tags', timeout=2)
                if models_response.status_code == 200:
                    models = models_response.json().get('models', [])
                    if models:
                        print(f"   Available models: {len(models)}")
                        for model in models[:3]:  # Show first 3 models
                            print(f"   - {model.get('name', 'Unknown')}")
                    else:
                        print("   No models installed. Run: ollama pull llama2")
            except:
                pass
            
            return True
    except:
        pass
    
    print("❌ Ollama not found or not running")
    print("📥 To install Ollama (completely free):")
    print("   1. Visit: https://ollama.com/download")
    print("   2. Or run: curl -fsSL https://ollama.com/install.sh | sh")
    print("   3. Then run: ollama pull llama2")
    return False

def setup_groq():
    """Setup Groq API key."""
    print("\n🚀 Groq Setup (Recommended - Fast & Free)")
    print("=" * 40)
    print("Groq offers fast inference with generous free limits!")
    print("Models available: LLaMA, Mixtral, Gemma")
    print("\n📋 To get your Groq API key:")
    print("1. Go to: https://console.groq.com/keys")
    print("2. Sign up (it's free!)")
    print("3. Create an API key")
    
    api_key = input("\n🔑 Enter your Groq API key (or press Enter to skip): ").strip()
    
    if api_key:
        if api_key.startswith('gsk_'):
            return ('GROQ_API_KEY', api_key)
        else:
            print("⚠️  Warning: Groq API keys usually start with 'gsk_'")
            return ('GROQ_API_KEY', api_key)
    
    return None

def setup_huggingface():
    """Setup Hugging Face API key."""
    print("\n🤗 Hugging Face Setup (Free)")
    print("=" * 30)
    print("Hugging Face offers free access to many AI models!")
    print("\n📋 To get your Hugging Face token:")
    print("1. Go to: https://huggingface.co/settings/tokens")
    print("2. Sign up (it's free!)")
    print("3. Create a new token")
    
    api_key = input("\n🔑 Enter your Hugging Face token (or press Enter to skip): ").strip()
    
    if api_key:
        return ('HUGGINGFACE_API_KEY', api_key)
    
    return None

def setup_openrouter():
    """Setup OpenRouter API key."""
    print("\n🌐 OpenRouter Setup (Free Tier)")
    print("=" * 32)
    print("OpenRouter offers free access to multiple AI models!")
    print("Free models include LLaMA, Mistral, and more")
    print("\n📋 To get your OpenRouter API key:")
    print("1. Go to: https://openrouter.ai/keys")
    print("2. Sign up (free tier available)")
    print("3. Create an API key")
    
    api_key = input("\n🔑 Enter your OpenRouter API key (or press Enter to skip): ").strip()
    
    if api_key:
        if api_key.startswith('sk-or-'):
            return ('OPENROUTER_API_KEY', api_key)
        else:
            print("⚠️  Warning: OpenRouter API keys usually start with 'sk-or-'")
            return ('OPENROUTER_API_KEY', api_key)
    
    return None

def update_env_file(api_keys):
    """Update .env file with API keys."""
    if not api_keys:
        print("No API keys to update.")
        return
    
    # Create .env file if it doesn't exist
    if not os.path.exists('.env'):
        if os.path.exists('.env.example'):
            import shutil
            shutil.copy('.env.example', '.env')
            print("✅ Created .env file from template")
        else:
            with open('.env', 'w') as f:
                f.write("# Voice Assistant Environment Variables\n")
            print("✅ Created new .env file")
    
    # Read existing content
    with open('.env', 'r') as f:
        lines = f.readlines()
    
    # Update or add API keys
    updated_lines = []
    keys_added = set()
    
    for line in lines:
        updated = False
        for key_name, key_value in api_keys:
            if line.startswith(f'{key_name}='):
                updated_lines.append(f'{key_name}={key_value}\n')
                keys_added.add(key_name)
                updated = True
                break
        if not updated:
            updated_lines.append(line)
    
    # Add new keys that weren't found
    for key_name, key_value in api_keys:
        if key_name not in keys_added:
            updated_lines.append(f'{key_name}={key_value}\n')
    
    # Write updated file
    with open('.env', 'w') as f:
        f.writelines(updated_lines)
    
    print(f"✅ Updated .env file with {len(api_keys)} API key(s)")

def main():
    """Main setup function."""
    print("🚀 Free AI Providers Setup")
    print("Choose from multiple free AI services for your voice assistant!")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists('voice_assistant_free.py'):
        print("❌ voice_assistant_free.py not found!")
        print("📂 Please run this script from the voice-assistant directory")
        sys.exit(1)
    
    api_keys = []
    
    # Check Ollama first (completely free, local)
    print("🏠 Checking for local Ollama installation...")
    ollama_available = check_ollama()
    
    if ollama_available:
        print("🎉 Great! You can use Ollama for completely free AI!")
        print("   No API key needed - it runs on your computer")
    
    print("\n" + "=" * 60)
    print("🌐 Let's set up cloud-based free AI providers:")
    
    # Setup cloud providers
    groq_key = setup_groq()
    if groq_key:
        api_keys.append(groq_key)
    
    hf_key = setup_huggingface()
    if hf_key:
        api_keys.append(hf_key)
    
    openrouter_key = setup_openrouter()
    if openrouter_key:
        api_keys.append(openrouter_key)
    
    # Update .env file
    if api_keys:
        update_env_file(api_keys)
    
    print("\n" + "=" * 60)
    print("🎯 Setup Complete!")
    
    if ollama_available or api_keys:
        print("✅ You have at least one free AI provider configured!")
        print("\n🚀 Next steps:")
        print("1. Test your setup: python test_setup.py")
        print("2. Run your voice assistant: python voice_assistant_free.py")
    else:
        print("⚠️  No AI providers configured.")
        print("💡 Recommendation: Try Groq first - it's fast and has generous free limits!")
    
    print("\n📊 Free Provider Comparison:")
    print("🚀 Groq:        Fast, generous limits, easy setup")
    print("🏠 Ollama:      Completely free, runs locally, no limits")
    print("🤗 Hugging Face: Many models, good for experimentation")
    print("🌐 OpenRouter:   Multiple models, free tier available")

if __name__ == "__main__":
    main()
