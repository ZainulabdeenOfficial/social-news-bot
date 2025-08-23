# 🤖 AI News Agent - Windows Executable

A standalone Windows executable that launches the AI News Agent web dashboard.

## 🚀 Quick Start

### 1. Download and Run

1. **Download** `AI_News_Agent.exe`
2. **Double-click** to run
3. **Web dashboard** opens automatically in your browser
4. **Configure** API keys in the Settings tab

### 2. First Time Setup

1. **Run the executable**
2. **Wait** for the dashboard to load (may take 10-30 seconds)
3. **Go to Settings tab** in the web dashboard
4. **Enter your API keys**:
   - OpenAI API Key (required)
   - LinkedIn credentials (optional)
   - Twitter credentials (optional)
5. **Save settings** and start using!

## 📋 What You Need

### Required
- **OpenAI API Key**: Get from [OpenAI Platform](https://platform.openai.com/api-keys)
- **Windows 10/11**: The executable is designed for Windows

### Optional
- **LinkedIn API**: For posting to LinkedIn
- **Twitter API**: For posting to Twitter
- **Facebook API**: For posting to Facebook

## 🎯 Features

- ✅ **No Python Required**: Standalone executable
- ✅ **Web Dashboard**: Beautiful interface in browser
- ✅ **API Configuration**: Easy setup through UI
- ✅ **News Fetching**: Automated tech news collection
- ✅ **AI Content**: GPT-4 powered post generation
- ✅ **Image Generation**: DALL-E 3 custom images
- ✅ **Social Media**: Multi-platform posting
- ✅ **Scheduling**: Automated posting times

## 🔧 Troubleshooting

### Common Issues

**"Application won't start"**
- Make sure you have Windows 10/11
- Try running as administrator
- Check Windows Defender isn't blocking it

**"Dashboard doesn't open"**
- Wait 10-30 seconds for startup
- Check if port 8501 is available
- Try refreshing the browser

**"API errors"**
- Verify your API keys are correct
- Check your internet connection
- Ensure you have API credits/quotas

**"Slow startup"**
- First run takes longer (downloading dependencies)
- Subsequent runs are faster
- Close other applications to free memory

### Getting Help

1. **Check the logs** in the console window
2. **Restart** the application
3. **Verify** your API keys
4. **Check** your internet connection

## 📁 File Structure

```
AI_News_Agent/
├── AI_News_Agent.exe          # Main executable
├── env_template.txt           # Configuration template
└── AI News Agent.bat          # Desktop shortcut (if installed)
```

## 🔒 Security

- **API Keys**: Stored locally in .env file
- **No Data Collection**: Application doesn't send data to external servers
- **Local Processing**: All AI processing done through your API keys
- **Privacy**: Your news sources and posts are private

## 🆘 Support

If you need help:

1. **Check this README** for common solutions
2. **Look at the console** for error messages
3. **Verify your setup** matches the requirements
4. **Contact support** with specific error details

## 📝 License

This executable is provided as-is for personal use. Please respect the terms of service for all APIs used.

---

**Made with ❤️ by AI News Agent Team**

*Transform your social media presence with AI-powered tech news automation!*
