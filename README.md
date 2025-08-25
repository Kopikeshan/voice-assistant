# 🎭 Custom Voice Assistant

A personalized voice assistant that lets you create your own AI personality.

## ✨ Features

- 🎭 **Custom Personalities** - Create your own unique AI personality
- 🆓 **Free AI** - Uses free Groq API 
- 🎤 **Voice Input** - Continuous listening
- 🔊 **Voice Output** - Natural text-to-speech
- 💾 **Save Personalities** - Reuse your custom personalities

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Get a free Groq API key:**
   - Visit [console.groq.com](https://console.groq.com/keys)
   - Create account and get API key

3. **Configure:**
   ```bash
   cp .env.example .env
   # Add your GROQ_API_KEY to .env file
   ```

4. **Run:**
   ```bash
   python voice_assistant.py
   ```

## 🎯 Create Your Personality

When you first run the assistant, you'll create a personality:

1. **Name** - Give your assistant a name
2. **Behavior** - Describe how it should act
3. **Greeting** - What it says when starting

### Example Personalities

- **Sarcastic Helper**: "Be witty and sarcastic but still helpful"
- **Motivational Coach**: "Be energetic and encouraging"
- **Wise Mentor**: "Speak calmly and thoughtfully"
- **Pirate Assistant**: "Talk like a pirate but give good advice"

## 🎮 Usage

1. Start the assistant and create your personality
2. Speak naturally - it's always listening
3. Say "goodbye" or "exit" to stop

## 📁 Files

```
voice-assistant/
├── voice_assistant.py      # Main app
├── requirements.txt        # Dependencies  
├── .env.example           # Config template
├── .env                   # Your API key
├── custom_personality.json # Saved personality
├── check_setup.py         # Setup checker
└── README.md              # This file
```

## 🔧 Check Setup

Verify everything is working:
```bash
python check_setup.py
```

## 🆘 Troubleshooting

- **No microphone**: Check permissions and connection
- **Speech errors**: Check internet and speak clearly  
- **No AI provider**: Add GROQ_API_KEY to .env file
- **TTS issues**: Will fallback to macOS 'say' command

## 📜 License

MIT License - feel free to customize and contribute!
