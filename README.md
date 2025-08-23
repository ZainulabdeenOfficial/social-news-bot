![Social News Bot Banner](https://raw.githubusercontent.com/ZainulabdeenOfficial/social-news-bot/main/LogoBot.png)

# 🤖 AI News Agent

An intelligent automated system that fetches tech news, generates engaging social media posts using AI, and automatically posts to LinkedIn, Twitter, and other platforms at optimal times.

## 🚀 Quick Deploy - Choose Your Platform

### 🟣 Vercel (Recommended - Fastest)
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/ZainulabdeenOfficial/social-news-bot)

### 🚆 Railway (Easiest)
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/ZainulabdeenOfficial/social-news-bot)

### 🎨 Render (Most Reliable)
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/ZainulabdeenOfficial/social-news-bot)

### 🔵 Heroku (Classic)
[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/ZainulabdeenOfficial/social-news-bot)

**Or use our universal deployment script:**
```bash
python deploy.py
```

## ✨ Features

- 📰 **Automated News Fetching**: Fetches latest tech news from multiple sources
- 🤖 **AI Content Generation**: Uses OpenAI to create engaging social media posts
- 🎨 **Image Generation**: Creates professional images for each post
- 📱 **Multi-Platform Posting**: Posts to LinkedIn, Twitter, Facebook
- ⏰ **Smart Scheduling**: Posts at optimal times for maximum engagement
- 📊 **Dashboard Interface**: Beautiful web interface for monitoring and control
- 🔄 **Continuous Operation**: Runs 24/7 with automated scheduling

## 🛠️ Local Development

### Prerequisites
- Python 3.8+
- OpenAI API key
- Social media API keys (optional)

### Installation
```bash
# Clone the repository
git clone https://github.com/ZainulabdeenOfficial/social-news-bot.git
cd social-news-bot

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp env_template.txt .env
# Edit .env with your API keys
```

### Usage

#### Web Dashboard
```bash
streamlit run web_dashboard.py
```

#### Command Line Interface
```bash
# Start the automated scheduler
python main.py run

# Post content immediately
python main.py post-now

# Fetch recent news
python main.py fetch-news

# Test all components
python main.py test
```

## 🌐 Deployment Options

### 🟣 Vercel (Recommended)
- ⚡ Lightning fast deployments
- 🌍 Global CDN
- 🔄 Automatic deployments
- 📱 Serverless functions
- 🆓 Generous free tier

### 🚆 Railway
- 🎯 One-click deployment
- 🔧 Easy environment variable management
- 📊 Built-in monitoring
- 🆓 500 hours/month free
- 🔄 GitHub integration

### 🎨 Render
- 🛡️ DDoS protection
- 🔒 Automatic SSL
- 📈 Auto-scaling
- 🆓 750 hours/month free
- 🌐 Custom domains

### 🔵 Heroku
- 🏛️ Established platform
- 🔧 Extensive add-ons
- 📊 Advanced monitoring
- 🆓 550-1000 hours/month free
- 🛠️ CLI tools

**📖 For detailed deployment instructions, see:**
- [Multi-Platform Deployment Guide](MULTI_PLATFORM_DEPLOYMENT.md)
- [Vercel Deployment Guide](VERCEL_DEPLOYMENT_GUIDE.md)
- [Quick Deploy Guide](QUICK_DEPLOY.md)

## 🔧 Configuration

### Required Environment Variables
```bash
OPENAI_API_KEY=sk-your-openai-api-key-here
```

### Optional Environment Variables
```bash
# LinkedIn
LINKEDIN_CLIENT_ID=your_linkedin_client_id
LINKEDIN_CLIENT_SECRET=your_linkedin_client_secret
LINKEDIN_ACCESS_TOKEN=your_linkedin_access_token

# Twitter
TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET=your_twitter_api_secret
TWITTER_ACCESS_TOKEN=your_twitter_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret

# Facebook
FACEBOOK_ACCESS_TOKEN=your_facebook_access_token
FACEBOOK_PAGE_ID=your_facebook_page_id
```

## 📁 Project Structure

```
├── api/
│   └── index.py              # Vercel API endpoint
├── web_dashboard.py          # Streamlit web interface
├── main.py                   # CLI application
├── config.py                 # Configuration management
├── news_fetcher.py           # News fetching logic
├── content_generator.py      # AI content generation
├── image_generator.py        # Image generation
├── social_media_poster.py    # Social media posting
├── scheduler.py              # Scheduling logic
├── requirements.txt          # Python dependencies
├── vercel.json              # Vercel configuration
├── Procfile                 # Heroku configuration
├── railway.json             # Railway configuration
├── render.yaml              # Render configuration
├── runtime.txt              # Python version specification
├── deploy.py               # Universal deployment script
├── deploy_vercel.py        # Vercel-specific deployment script
└── README.md                # This file
```

## 🔍 API Endpoints

### Health Check
```
GET /health
```
Returns service status and version information.

### API Status
```
GET /api/status
```
Returns status of all components (news fetcher, content generator, etc.).

## 🚀 Performance

- **Fast Deployment**: Optimized for all major platforms
- **Auto-scaling**: Handles traffic spikes automatically
- **Global CDN**: Content delivered from edge locations
- **99.9% Uptime**: Reliable hosting infrastructure

## 🔒 Security

- **Environment Variables**: Secure API key management
- **HTTPS**: Automatic SSL certificates
- **Input Validation**: All inputs are validated
- **Rate Limiting**: Built-in protection against abuse

## 📊 Monitoring

- **Health Checks**: Automatic monitoring endpoints
- **Error Tracking**: Comprehensive error logging
- **Performance Metrics**: Real-time performance monitoring
- **Usage Analytics**: Track API usage and performance

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for providing the AI capabilities
- Streamlit for the web framework
- Vercel, Railway, Render, and Heroku for hosting platforms
- All contributors and supporters

## 📞 Support

- **Documentation**: [MULTI_PLATFORM_DEPLOYMENT.md](MULTI_PLATFORM_DEPLOYMENT.md)
- **Issues**: [GitHub Issues](https://github.com/ZainulabdeenOfficial/social-news-bot/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ZainulabdeenOfficial/social-news-bot/discussions)

---

**Made with ❤️ by M Zain Ul Abideen**

[![GitHub stars](https://img.shields.io/github/stars/ZainulabdeenOfficial/social-news-bot?style=social)](https://github.com/ZainulabdeenOfficial/social-news-bot)
[![GitHub forks](https://img.shields.io/github/forks/ZainulabdeenOfficial/social-news-bot?style=social)](https://github.com/ZainulabdeenOfficial/social-news-bot)
[![GitHub issues](https://img.shields.io/github/issues/ZainulabdeenOfficial/social-news-bot)](https://github.com/ZainulabdeenOfficial/social-news-bot/issues)
[![GitHub license](https://img.shields.io/github/license/ZainulabdeenOfficial/social-news-bot)](https://github.com/ZainulabdeenOfficial/social-news-bot/blob/main/LICENSE)

