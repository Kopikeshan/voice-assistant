#!/usr/bin/env python3
"""
Custom Voice Assistant with Personality and Wake Word Detection
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
import pvporcupine
import struct
from dotenv import load_dotenv

load_dotenv()

class VoiceAssistant:
    def __init__(self):
        print("🚀 Initializing Custom Voice Assistant...")
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.setup_tts_engine()  # Just initialize TTS engine
        self.provider = None
        self.api_key = None
        self.base_url = None
        self.model = None
        self.personality = None
        self.setup_wake_word()
        self.setup_ai_provider()
        self.setup_personality()
        self.setup_voice_selection()  # Set up voice after personality is loaded
        
    def setup_tts_engine(self):
        """Initialize TTS engine without voice selection."""
        try:
            self.tts_engine = pyttsx3.init()
            self.tts_method = 'pyttsx3'
            print("Text-to-speech engine initialized")
        except Exception as e:
            print(f"pyttsx3 failed: {e}")
            if platform.system() == 'Darwin':
                self.tts_method = 'say'
                print("Using macOS 'say' command")
            else:
                print("No text-to-speech available")
                sys.exit(1)
    
    def setup_voice_selection(self):
        """Set up voice selection after personality is loaded."""
        if self.tts_method == 'pyttsx3':
            self.setup_pyttsx3_voice_selection()
        else:
            self.setup_macos_voice_selection()
    
    def setup_pyttsx3_voice_selection(self):
        """Set up voice selection for pyttsx3."""
        voices = self.tts_engine.getProperty('voices')
        print(f"\nVoice selection for {self.personality['name']}:")
        print("Available voices:")
        for i, voice in enumerate(voices[:5]):  # Show first 5 voices
            print(f"{i+1}. {voice.name}")
        
        try:
            choice = input("\nSelect voice (1-5, or press Enter for default): ").strip()
            if choice and choice.isdigit() and 1 <= int(choice) <= len(voices):
                selected_voice = voices[int(choice)-1]
                self.tts_engine.setProperty('voice', selected_voice.id)
                print(f"Selected voice: {selected_voice.name}")
            else:
                print("Using default voice")
        except:
            print("Using default voice")
    
    def setup_macos_voice_selection(self):
        """Set up voice selection for macOS say command."""
        # Premium natural voices
        natural_voices = [
            ("Samantha", "Natural female voice (US English) - Recommended"),
            ("Karen", "Natural female voice (Australian English)"), 
            ("Moira", "Natural female voice (Irish English)"),
            ("Tessa", "Natural female voice (South African English)"),
            ("Alex", "Natural male voice (US English)")
        ]
        
        print(f"\nVoice selection for {self.personality['name']}:")
        print("Available natural voices:")
        for i, (voice, description) in enumerate(natural_voices):
            print(f"{i+1}. {voice} - {description}")
        
        try:
            choice = input(f"\nSelect voice (1-5, or press Enter for Samantha): ").strip()
            if choice and choice.isdigit() and 1 <= int(choice) <= len(natural_voices):
                self.selected_voice = natural_voices[int(choice)-1][0]
            else:
                self.selected_voice = "Samantha"  # Default to most natural female voice
                
            print(f"Selected voice: {self.selected_voice}")
            
            # Test the voice
            test_phrase = f"Hello! I'm {self.personality['name']}. This is how I sound."
            print("Testing voice...")
            subprocess.run(['say', '-v', self.selected_voice, test_phrase], check=True)
            
        except Exception as e:
            print(f"Voice selection failed: {e}")
            self.selected_voice = "Samantha"
            print("Using default Samantha voice")
    
    def setup_wake_word(self):
        """Initialize wake word detection with Porcupine or fallback to simple detection."""
        try:
            print("Setting up wake word detection...")
            
            # Try to get Porcupine access key
            access_key = os.getenv('PORCUPINE_ACCESS_KEY')
            
            if access_key and access_key != 'your_porcupine_key_here':
                # Use advanced Porcupine wake word detection
                self.porcupine = pvporcupine.create(
                    access_key=access_key,
                    keywords=['computer', 'jarvis']  # Built-in keywords
                )
                self.wake_word_method = 'porcupine'
                self.wake_word_active = True
                print("Advanced wake word detection ready - say 'Computer' or 'Jarvis'")
                return
            else:
                print("No Porcupine access key found.")
                print("Get a free key from: https://console.picovoice.ai/")
                print("Add PORCUPINE_ACCESS_KEY to your .env file for advanced wake words")
                
        except Exception as e:
            print(f"Porcupine setup failed: {e}")
        
        # Fallback to simple speech recognition wake word
        print("Using simple wake word detection instead")
        assistant_name = "your assistant"  # Default before personality is loaded
        print(f"Wake phrases will be set to use your assistant's name once personality is loaded")
        self.porcupine = None
        self.wake_word_method = 'simple'
        self.wake_word_active = True
    
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
    
    def listen_for_wake_word(self):
        """Listen continuously for wake word using available method."""
        if self.wake_word_method == 'porcupine' and self.porcupine:
            return self.listen_for_wake_word_porcupine()
        else:
            return self.listen_for_wake_word_simple()
    
    def listen_for_wake_word_simple(self):
        """Simple wake word detection using speech recognition."""
        # Create wake phrases using the assistant's name
        assistant_name = self.personality['name'].lower()
        wake_phrases = [
            assistant_name,                    # Just the name: "hinata"
            f"hey {assistant_name}",          # Hey + name: "hey hinata"  
            f"hi {assistant_name}",           # Hi + name: "hi hinata"
            f"{assistant_name} wake up",      # Name + wake up: "hinata wake up"
            'wake up',                        # Generic fallback
            'assistant'                       # Generic fallback
        ]
        
        print(f"Sleeping... Say '{assistant_name}', 'hey {assistant_name}', or 'wake up' to wake me up")
        
        while True:
            try:
                with self.microphone as source:
                    # Listen for audio with a shorter timeout for wake words
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=3)
                
                # Try to recognize what was said
                text = self.recognizer.recognize_google(audio).lower()
                
                # Check if any wake phrase was detected
                for phrase in wake_phrases:
                    if phrase in text:
                        print(f"Wake word detected: '{phrase}'")
                        self.speak("Yes? I'm listening.")
                        return True
                        
            except sr.WaitTimeoutError:
                # No speech detected, continue listening
                continue
            except sr.UnknownValueError:
                # Speech was unclear, continue listening  
                continue
            except KeyboardInterrupt:
                print("\nGoing to sleep...")
                return False
            except Exception as e:
                print(f"Wake word error: {e}")
                time.sleep(1)
                continue
    
    def listen_for_wake_word_porcupine(self):
        """Advanced wake word detection using Porcupine."""
        if not self.porcupine:
            return self.listen_for_wake_word_simple()
            
        import pyaudio
        
        print("Sleeping... Say 'Computer' or 'Jarvis' to wake me up")
        
        pa = pyaudio.PyAudio()
        audio_stream = pa.open(
            rate=self.porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=self.porcupine.frame_length
        )
        
        try:
            while True:
                pcm = audio_stream.read(self.porcupine.frame_length)
                pcm = struct.unpack_from("h" * self.porcupine.frame_length, pcm)
                
                keyword_index = self.porcupine.process(pcm)
                if keyword_index >= 0:
                    print("Wake word detected! I'm listening...")
                    self.speak("Yes?")
                    audio_stream.stop_stream()
                    audio_stream.close()
                    pa.terminate()
                    return True
                    
        except KeyboardInterrupt:
            print("\nGoing to sleep...")
            return False
        finally:
            try:
                audio_stream.stop_stream()
                audio_stream.close()
                pa.terminate()
            except:
                pass
                pass
    
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
        """Convert text to speech using selected voice."""
        try:
            if self.tts_method == 'pyttsx3':
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            elif self.tts_method == 'say':
                # Use selected voice if available, otherwise default
                voice = getattr(self, 'selected_voice', 'Samantha')
                subprocess.run(['say', '-v', voice, text], check=True)
        except Exception as e:
            print(f"TTS Error: {e}")
            print(f"🤖 {text}")
    
    def run(self):
        """Main run method with wake word detection."""
        print(f"\n{'='*50}")
        print(f"🎭 {self.personality['name']} is ready!")
        print(f"💭 {self.personality['prompt']}")
        print(f"{'='*50}")
        
        print(f"\n🤖 {self.personality['greeting']}")
        self.speak(self.personality['greeting'])
        
        if self.wake_word_active:
            assistant_name = self.personality['name']
            print(f"\n💤 Wake word mode enabled - say '{assistant_name}', 'hey {assistant_name}', or 'wake up' to activate")
        else:
            print("\n🎤 Listening continuously... Say 'goodbye' to exit")
        
        while True:
            # Wake word detection phase
            if self.wake_word_active:
                if not self.listen_for_wake_word():
                    break  # User pressed Ctrl+C
                
                # Now in active conversation mode
                print("🎤 I'm awake! What can I help you with? (Say 'sleep' to go back to sleep)")
                conversation_active = True
                last_activity = time.time()
                
                while conversation_active:
                    user_input = self.listen()
                    
                    if user_input:
                        last_activity = time.time()
                        
                        if any(word in user_input.lower() for word in ['goodbye', 'exit', 'stop']):
                            farewell = "Goodbye! Take care!"
                            print(f"🤖 {farewell}")
                            self.speak(farewell)
                            return  # Exit completely
                        
                        if any(word in user_input.lower() for word in ['sleep', 'go to sleep', 'wake word']):
                            print("💤 Going back to sleep mode...")
                            self.speak("Going back to sleep. Say the wake word to wake me up.")
                            conversation_active = False
                            continue
                        
                        print("🤖 Thinking...")
                        response = self.get_ai_response(user_input)
                        print(f"🤖 {self.personality['name']}: {response}")
                        self.speak(response)
                    
                    # Auto-sleep after 30 seconds of inactivity
                    if time.time() - last_activity > 30:
                        print("💤 Auto-sleeping due to inactivity...")
                        self.speak("Going back to sleep due to inactivity.")
                        conversation_active = False
                    
                    time.sleep(0.1)
            
            else:
                # Fallback to continuous listening if wake word not available
                user_input = self.listen()
                
                if user_input:
                    if any(word in user_input.lower() for word in ['goodbye', 'exit', 'stop']):
                        farewell = "Goodbye! Take care!"
                        print(f"🤖 {farewell}")
                        self.speak(farewell)
                        break
                    
                    print("🤖 Thinking...")
                    response = self.get_ai_response(user_input)
                    print(f"🤖 {self.personality['name']}: {response}")
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
