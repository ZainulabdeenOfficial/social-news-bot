
# 🤖 AI News Agent

An intelligent automated system that fetches tech news, generates engaging social media posts with AI, creates professional images, and automatically shares them on LinkedIn, Twitter, and other platforms.

## ✨ Features

- **📰 Automated News Fetching**: Scrapes tech news from multiple sources (TechCrunch, The Verge, Wired, etc.)
- **🤖 AI-Powered Content Generation**: Creates engaging posts using OpenAI's GPT-4
- **🎨 Professional Image Generation**: Generates custom images using DALL-E 3
- **📱 Multi-Platform Posting**: Posts to LinkedIn, Twitter, Facebook, and more
- **⏰ Smart Scheduling**: Automatically posts at optimal times for maximum engagement
- **📊 Beautiful Dashboard**: Web-based dashboard for monitoring and control
- **🔄 Daily Summaries**: Generates and posts daily tech news summaries
- **🎯 Trending Analysis**: Identifies and leverages trending topics

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd ai-news-agent

# Install dependencies
pip install -r requirements.txt

# Run setup script (optional but recommended)
python setup.py
```

### 2. Configuration

#### Option A: Web Dashboard (Recommended)
```bash
# Start the web dashboard
streamlit run web_dashboard.py
```

Then navigate to the **⚙️ Settings** tab to:
- Enter your API keys and social media credentials
- Configure posting schedules
- Test API connections
- Monitor configuration status

#### Option B: Manual Configuration
```bash
# Run the setup wizard
python main.py setup
```

Or copy the template and edit manually:
```bash
# Copy the template

# Edit with your API keys
```

Required configuration in `.env`:
```env
# Required: OpenAI API Key
OPENAI_API_KEY=your_openai_api_key_here

# Optional: LinkedIn API
LINKEDIN_CLIENT_ID=your_linkedin_client_id
LINKEDIN_CLIENT_SECRET=your_linkedin_client_secret
LINKEDIN_ACCESS_TOKEN=your_linkedin_access_token

# Optional: Twitter API
TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET=your_twitter_api_secret
TWITTER_ACCESS_TOKEN=your_twitter_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret

# Optional: Facebook API
FACEBOOK_ACCESS_TOKEN=your_facebook_access_token
FACEBOOK_PAGE_ID=your_facebook_page_id
```

### 3. Test the System

```bash
# Test all components
python main.py test

# Fetch recent news
python main.py fetch-news

# Post content immediately
python main.py post-now
```

### 4. Start the Automated System

```bash
# Start the scheduler (runs continuously)
python main.py run
```

### 5. Launch the Web Dashboard

```bash
# Start the beautiful web dashboard
streamlit run web_dashboard.py
```

## 📋 Usage

### Command Line Interface

```bash
# Start automated scheduler
python main.py run

# Post content immediately
python main.py post-now [--platform linkedin|twitter|facebook]

# Fetch and display news
python main.py fetch-news [--hours 24] [--limit 10]

# Test all components
python main.py test

# Setup configuration
python main.py setup

# Show system status
python main.py status
```

### Web Dashboard

The web dashboard provides a beautiful interface for:

- **📊 Overview**: System metrics, charts, and recent activity
- **📰 News Feed**: Browse and filter latest tech news
- **📝 Content Generator**: Test and generate content manually
- **📱 Social Media**: Manage posts and monitor platforms
- **⚙️ Settings**: 
  - Configure API keys and social media credentials
  - Set posting schedules
  - Test API connections
  - Monitor configuration status
  - Add news sources (read-only display)

### News Sources

        'category': 'tech'
    },
    # Add more sources...


```python
POSTING_SCHEDULE = {
    'linkedin': ['09:00', '12:00', '15:00', '18:00'],
    'twitter': ['08:00', '11:00', '14:00', '17:00', '20:00'],
    'facebook': ['10:00', '13:00', '16:00', '19:00']
}
```

### Content Settings

Customize content generation:

```python
MAX_POSTS_PER_DAY = 5
POST_LENGTH_LIMIT = {
    'linkedin': 3000,
    'twitter': 280,
    'facebook': 2000
}
```

## 🖥️ Windows Executable

### Create Standalone .exe File

To create a Windows executable that doesn't require Python installation:

```bash
# Method 1: Using the batch file (Recommended)
build_exe.bat

# Method 2: Using Python script
python build_exe.py

# Method 3: Manual PyInstaller
pip install pyinstaller
pyinstaller --onefile --console --name="AI_News_Agent" exe_launcher.py
```

### Install the Executable

```bash
# Run the installer
install_exe.bat
```

### Using the Executable

1. **Double-click** `AI_News_Agent.exe` or the desktop shortcut
2. **Web dashboard** will automatically open in your browser
3. **Configure API keys** in the Settings tab
4. **Start using** the AI News Agent

### Features of the Executable

- ✅ **Standalone**: No Python installation required
- ✅ **Self-contained**: All dependencies included
- ✅ **Easy to use**: Double-click to run
- ✅ **Web interface**: Beautiful dashboard in browser
- ✅ **Configuration**: API keys managed through UI
- ✅ **Portable**: Can be copied to any Windows machine

## 🚀 Free Deployment Options

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Deploy
railway up
```

### 2. Render

1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `python main.py run`

### 3. Heroku

```bash
# Install Heroku CLI
# Create Procfile
echo "worker: python main.py run" > Procfile

# Deploy
heroku create your-app-name
git push heroku main
```

### 4. Python Anywhere

1. Upload your code to PythonAnywhere
2. Install dependencies in a virtual environment
3. Set up a scheduled task to run `python main.py run`

## 📊 Monitoring and Analytics

The system provides comprehensive monitoring:

- **Real-time Metrics**: Articles fetched, posts published, engagement rates
- **Activity Logs**: Detailed logs of all operations
- **Error Tracking**: Automatic error detection and reporting
- **Performance Analytics**: Response times and success rates

## 🔒 Security Features

- **API Key Encryption**: Secure storage of sensitive credentials
- **Rate Limiting**: Respectful API usage to avoid rate limits
- **Error Handling**: Graceful handling of API failures
- **Logging**: Comprehensive audit trail

## 🛠️ Development

### Project Structure

```
ai-news-agent/
├── main.py                 # Main application entry point
├── config.py              # Configuration settings
├── news_fetcher.py        # News scraping and parsing
├── content_generator.py   # AI content generation
├── image_generator.py     # Image generation with DALL-E
├── social_media_poster.py # Social media posting
├── scheduler.py           # Automated scheduling
├── web_dashboard.py       # Streamlit web dashboard
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── .env                  # Environment variables (create this)
```

### Adding New Features

1. **New News Sources**: Add to `NEWS_SOURCES` in `config.py`
2. **New Social Platforms**: Extend `SocialMediaPoster` class
3. **Custom Content Templates**: Modify `ContentGenerator` class
4. **Additional Analytics**: Extend dashboard with new metrics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -am 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- **Documentation**: Check this README and code comments
- **Issues**: Report bugs and feature requests on GitHub
- **Discussions**: Join community discussions for help

## 🎯 Roadmap

- [ ] Instagram integration
- [ ] YouTube Shorts automation
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] Custom AI models
- [ ] Mobile app
- [ ] Team collaboration features

## 🙏 Acknowledgments

- OpenAI for GPT-4 and DALL-E 3
- Streamlit for the beautiful dashboard
- All the tech news sources for their RSS feeds
- The open-source community for inspiration

---

**Made with ❤️ by AI News Agent Team**

*Transform your social media presence with AI-powered tech news automation!*
=======
# social-news-bot
>>>>>>> c0e847343c7d6484acbdfb78d455262237a2f1d9
