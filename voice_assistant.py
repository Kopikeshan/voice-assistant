#!/usr/bin/env python3
"""
Custom Voice Assistant with Personality
"""

import os
import sys
import json
import time
import platform
import subprocess
import requests
import speech_recognition as sr
import pyttsx3
from dotenv import load_dotenv

load_dotenv()

class VoiceAssistant:
    def __init__(self):
        print("🚀 Initializing Custom Voice Assistant...")
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.setup_tts()
        self.provider = None
        self.api_key = None
        self.base_url = None
        self.model = None
        self.personality = None
        self.setup_ai_provider()
        self.setup_personality()
        
    def setup_tts(self):
        """Configure text-to-speech with macOS fallback."""
        try:
            self.tts_engine = pyttsx3.init()
            self.tts_method = 'pyttsx3'
            print("✅ Text-to-speech ready")
        except Exception as e:
            print(f"⚠️  pyttsx3 failed: {e}")
            if platform.system() == 'Darwin':
                self.tts_method = 'say'
                print("✅ Using macOS 'say' command")
            else:
                print("❌ No text-to-speech available")
                sys.exit(1)
    
    def setup_ai_provider(self):
        """Detect and configure available AI providers."""
        print("🔍 Detecting AI providers...")
        
        groq_key = os.getenv('GROQ_API_KEY')
        if groq_key and groq_key != 'your_groq_api_key_here':
            self.provider = 'groq'
            self.api_key = groq_key
            self.base_url = 'https://api.groq.com/openai/v1/chat/completions'
            self.model = 'llama-3.1-8b-instant'
            print("🚀 Using Groq (Free & Fast)")
            return
        
        print("❌ No AI provider configured!")
        print("Please set up Groq: https://console.groq.com/keys")
        sys.exit(1)
    
    def setup_personality(self):
        """Set up custom personality."""
        if self.load_saved_personality():
            use_saved = input("\n🔄 Found saved personality. Use it? (y/n): ").strip().lower()
            if use_saved in ['y', 'yes']:
                print(f"✅ Loaded: {self.personality['name']}")
                return
        
        print("\n🎭 Create Your Assistant's Personality")
        print("=" * 50)
        
        name = input("\n📝 Give your assistant a name: ").strip()
        if not name:
            name = "My Assistant"
        
        print(f"\n🧠 Describe {name}'s personality:")
        print("   Examples:")
        print("   - 'Be sarcastic and witty but helpful'")
        print("   - 'Act like a wise mentor'")
        print("   - 'Be energetic and motivational'")
        
        personality_prompt = input(f"\n   How should {name} behave? ").strip()
        if not personality_prompt:
            personality_prompt = "Be helpful and friendly."
        
        greeting = input(f"\n💬 What should {name} say when starting? ").strip()
        if not greeting:
            greeting = f"Hello! I'm {name}, your personal assistant."
        
        self.personality = {
            'name': name,
            'prompt': personality_prompt,
            'greeting': greeting
        }
        
        print(f"\n✨ {name} is ready!")
        
        save = input(f"\n💾 Save {name} for future use? (y/n): ").strip().lower()
        if save in ['y', 'yes']:
            self.save_custom_personality()
    
    def load_saved_personality(self):
        """Load saved personality."""
        try:
            with open('custom_personality.json', 'r') as f:
                self.personality = json.load(f)
            return True
        except:
            return False
    
    def save_custom_personality(self):
        """Save personality."""
        try:
            with open('custom_personality.json', 'w') as f:
                json.dump(self.personality, f, indent=2)
            print("✅ Personality saved")
        except Exception as e:
            print(f"⚠️ Couldn't save: {e}")
    
    def listen(self):
        """Listen for voice input."""
        try:
            print("🎧 Listening...")
            with self.microphone as source:
                audio = self.recognizer.listen(source, phrase_time_limit=15)
            
            print("🔄 Processing...")
            text = self.recognizer.recognize_google(audio)
            print(f"👤 You: {text}")
            return text
        except sr.UnknownValueError:
            print("🤔 Couldn't understand that")
            return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def get_ai_response(self, user_input):
        """Get AI response."""
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            system_prompt = "You are a helpful voice assistant. Be concise and friendly."
            if self.personality:
                system_prompt = f"{self.personality['prompt']} {system_prompt}"
            
            data = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                "max_tokens": 150,
                "temperature": 0.7
            }
            
            response = requests.post(self.base_url, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content'].strip()
            else:
                return "Sorry, I'm having trouble right now."
        except Exception as e:
            print(f"❌ AI Error: {e}")
            return "I'm having trouble processing that."
    
    def speak(self, text):
        """Convert text to speech."""
        try:
            if self.tts_method == 'pyttsx3':
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            elif self.tts_method == 'say':
                subprocess.run(['say', text], check=True)
        except Exception as e:
            print(f"❌ TTS Error: {e}")
            print(f"🤖 {text}")
    
    def run(self):
        """Main run method."""
        print(f"\n{'='*50}")
        print(f"🎭 {self.personality['name']} is ready!")
        print(f"💭 {self.personality['prompt']}")
        print(f"{'='*50}")
        
        print(f"\n🤖 {self.personality['greeting']}")
        self.speak(self.personality['greeting'])
        
        print("\n🎤 Listening continuously... Say 'goodbye' to exit")
        
        while True:
            user_input = self.listen()
            
            if user_input:
                if any(word in user_input.lower() for word in ['goodbye', 'exit', 'stop']):
                    farewell = "Goodbye! Take care!"
                    print(f"🤖 {farewell}")
                    self.speak(farewell)
                    break
                
                print("🤖 Thinking...")
                response = self.get_ai_response(user_input)
                print(f"�� {self.personality['name']}: {response}")
                self.speak(response)
            
            time.sleep(0.1)

def main():
    try:
        assistant = VoiceAssistant()
        assistant.run()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
