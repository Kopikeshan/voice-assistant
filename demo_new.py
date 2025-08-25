#!/usr/bin/env python3
"""
Demo Voice Assistant (No AI required)
Test your microphone and text-to-speech without needing an AI API key.
"""

import speech_recognition as sr
import pyttsx3
import time
import subprocess
import platform

class DemoVoiceAssistant:
    def __init__(self):
        """Initialize the demo voice assistant."""
        print("🎤 Initializing Demo Voice Assistant...")
        
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Initialize text-to-speech
        self.setup_tts()
        
        # Adjust for ambient noise
        print("🔧 Adjusting for ambient noise...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
        print("✅ Ready to listen!")
        
    def setup_tts(self):
        """Configure text-to-speech settings with multiple fallback options."""
        self.tts_method = None
        self.tts_engine = None
        
        # Try pyttsx3 first
        try:
            import pyttsx3
            self.tts_engine = pyttsx3.init()
            
            # Set speech rate and volume
            self.tts_engine.setProperty('rate', 180)
            self.tts_engine.setProperty('volume', 0.9)
            
            # Test pyttsx3 quietly
            self.tts_method = "pyttsx3"
            print("✅ Text-to-speech initialized with pyttsx3")
            
        except Exception as e:
            print(f"⚠️  pyttsx3 failed: {e}")
            
            # Fallback to macOS built-in 'say' command
            if platform.system() == "Darwin":  # macOS
                try:
                    subprocess.run(['say', 'Testing'], check=True, capture_output=True, timeout=5)
                    self.tts_method = "macos_say"
                    print("✅ Text-to-speech initialized with macOS 'say' command")
                except Exception as say_error:
                    print(f"⚠️  macOS 'say' command failed: {say_error}")
                    self.tts_method = "text_only"
                    print("📝 Text-to-speech disabled, will use text output only")
            else:
                self.tts_method = "text_only"
                print("📝 Text-to-speech disabled, will use text output only")
    
    def listen(self):
        """Listen for audio input and convert to text."""
        try:
            print("🎧 Listening... (speak now)")
            with self.microphone as source:
                # Listen for audio with timeout
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            print("🔄 Processing speech...")
            # Convert speech to text using Google Speech Recognition
            text = self.recognizer.recognize_google(audio)
            print(f"📝 You said: '{text}'")
            return text.lower()
            
        except sr.WaitTimeoutError:
            print("⏰ No speech detected within timeout period.")
            return None
        except sr.UnknownValueError:
            print("❓ Could not understand the audio.")
            return None
        except sr.RequestError as e:
            print(f"❌ Error with speech recognition service: {e}")
            return None
    
    def speak(self, text):
        """Convert text to speech and play it using the best available method."""
        print(f"🤖 Assistant: {text}")
        
        if self.tts_method == "pyttsx3" and self.tts_engine:
            try:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
                return
            except Exception as e:
                print(f"⚠️  pyttsx3 error, falling back: {e}")
                self.tts_method = "macos_say"
        
        if self.tts_method == "macos_say" and platform.system() == "Darwin":
            try:
                # Use macOS built-in 'say' command with a nice voice
                subprocess.run(['say', '-v', 'Samantha', text], check=True, timeout=10)
                return
            except Exception as e:
                print(f"⚠️  macOS 'say' error: {e}")
                self.tts_method = "text_only"
        
        # Text-only fallback
        print("🔇 (Speaking not available, text output only)")
    
    def handle_command(self, command):
        """Process voice commands and return simple responses."""
        if not command:
            return True
        
        # Check for exit commands
        if any(word in command for word in ['exit', 'quit', 'goodbye', 'bye', 'stop']):
            self.speak("Goodbye! Demo completed successfully!")
            return False
        
        # Demo responses
        if 'hello' in command or 'hi' in command:
            self.speak("Hello! This is your demo voice assistant. I can speak back to you now!")
            return True
        
        if 'test' in command:
            self.speak("Test successful! Your microphone and speakers are working great!")
            return True
        
        if 'time' in command:
            current_time = time.strftime("%I:%M %p")
            self.speak(f"The current time is {current_time}")
            return True
        
        if 'date' in command:
            current_date = time.strftime("%B %d, %Y")
            self.speak(f"Today is {current_date}")
            return True
        
        if 'name' in command:
            self.speak("I'm your demo voice assistant. I'm testing your setup and I can talk back!")
            return True
        
        if 'voice' in command or 'speak' in command:
            self.speak("Yes! I can speak back to you now. Your voice assistant is working perfectly!")
            return True
        
        # Echo back what was said
        self.speak(f"You said: {command}. This proves your voice assistant is working and can talk back!")
        return True
    
    def run(self):
        """Main demo loop."""
        print("🎙️  Demo Voice Assistant Started!")
        print("💡 This demo doesn't need AI - it's testing your hardware")
        print("🔊 Your assistant will now SPEAK BACK to you!")
        print("📋 Try saying: 'hello', 'test', 'time', 'date', or anything else")
        print("🛑 Say 'exit' or 'goodbye' to stop")
        print("-" * 60)
        
        self.speak("Demo voice assistant ready! I can now speak back to you. Your microphone and speakers are being tested.")
        
        demo_count = 0
        max_demos = 10  # Limit demo interactions
        
        while demo_count < max_demos:
            try:
                print(f"\n🔄 Demo {demo_count + 1}/{max_demos}")
                
                # Listen for voice input
                user_input = self.listen()
                
                if user_input:
                    # Process the command
                    demo_count += 1
                    continue_running = self.handle_command(user_input)
                    if not continue_running:
                        break
                else:
                    # If no input detected, continue listening
                    continue
                    
            except KeyboardInterrupt:
                print("\n👋 Demo stopped by user!")
                self.speak("Demo stopped. Everything looks good!")
                break
            except Exception as e:
                print(f"❌ Unexpected error: {e}")
                
        if demo_count >= max_demos:
            print(f"\n🎉 Demo completed! ({max_demos} interactions)")
            self.speak("Demo completed successfully! Your voice assistant hardware is working perfectly and I can talk back to you!")

def main():
    """Main function to start the demo."""
    print("🚀 Starting Demo Voice Assistant...")
    print("🔊 This tests your microphone AND speakers - the assistant will talk back!")
    
    try:
        assistant = DemoVoiceAssistant()
        assistant.run()
        print("\n✅ Demo completed successfully!")
        print("🎯 Your voice assistant can now speak back to you!")
        print("   Next step: Set up an AI API and run the full voice assistant")
        print("   Run: python setup_free.py for FREE AI options")
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        print("🔧 Please check your microphone and speaker connections")

if __name__ == "__main__":
    main()
