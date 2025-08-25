#!/usr/bin/env python3
"""
Simple test to verify voice assistant initialization
"""

from voice_assistant import VoiceAssistant

print("Starting test...")
try:
    assistant = VoiceAssistant()
    print("Assistant created successfully!")
    print(f"Provider: {assistant.provider}")
    print(f"Personality: {assistant.personality}")
except Exception as e:
    print(f"Error: {e}")
