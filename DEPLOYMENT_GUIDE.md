# 🚀 AI News Agent - Deployment Guide

This guide will help you deploy your AI News Agent to various free hosting platforms.

## 📋 Prerequisites

- ✅ Code pushed to GitHub: [https://github.com/ZainulabdeenOfficial/social-news-bot](https://github.com/ZainulabdeenOfficial/social-news-bot)
- ✅ OpenAI API key (for content and image generation)
- ✅ Social media API keys (LinkedIn, Twitter, Facebook) - optional but recommended

## 🆓 Free Deployment Options

### 1. 🚆 Railway (Recommended - Easiest)

Railway offers generous free tier with automatic deployments.

#### Steps:
1. **Visit Railway**: Go to [railway.app](https://railway.app)
2. **Sign Up**: Use your GitHub account
3. **Deploy from GitHub**:
   - Click "Deploy from GitHub"
   - Select your repository: `ZainulabdeenOfficial/social-news-bot`
   - Railway will automatically detect the configuration
4. **Set Environment Variables**:
   ```
   OPENAI_API_KEY=your_openai_api_key
   LINKEDIN_ACCESS_TOKEN=your_linkedin_token
   TWITTER_API_KEY=your_twitter_key
   TWITTER_API_SECRET=your_twitter_secret
   TWITTER_ACCESS_TOKEN=your_twitter_access_token
   TWITTER_ACCESS_TOKEN_SECRET=your_twitter_token_secret
   ```
5. **Deploy**: Railway will automatically build and deploy
6. **Access**: Your app will be available at a Railway-provided URL

#### Features:
- ✅ 500 hours/month free
- ✅ Automatic deployments on GitHub push
- ✅ Built-in domain and SSL
- ✅ Easy environment variable management

---

### 2. 🎨 Render (Great Alternative)

Render provides reliable free hosting with excellent performance.

#### Steps:
1. **Visit Render**: Go to [render.com](https://render.com)
2. **Sign Up**: Connect your GitHub account
3. **Create Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select `ZainulabdeenOfficial/social-news-bot`
4. **Configure Service**:
   - Name: `ai-news-agent`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run web_dashboard.py --server.port=$PORT --server.address=0.0.0.0`
5. **Set Environment Variables** (same as Railway)
6. **Deploy**: Click "Create Web Service"

#### Features:
- ✅ 750 hours/month free
- ✅ Automatic SSL certificates
- ✅ GitHub integration
- ✅ DDoS protection

---

### 3. 🟣 Heroku (Classic Option)

Heroku is the classic choice for app deployment.

#### Steps:
1. **Install Heroku CLI**: Download from [heroku.com](https://heroku.com)
2. **Login**: `heroku login`
3. **Create App**: `heroku create your-ai-news-agent`
4. **Set Config Vars**:
   ```bash
   heroku config:set OPENAI_API_KEY=your_key
   heroku config:set LINKEDIN_ACCESS_TOKEN=your_token
   # ... add other environment variables
   ```
5. **Deploy**: 
   ```bash
   git push heroku main
   ```

#### Features:
- ✅ 550-1000 dyno hours/month free
- ✅ Add-ons marketplace
- ✅ CLI tools

---

### 4. ☁️ Google Cloud Run (Serverless)

Perfect for variable traffic patterns.

#### Steps:
1. **Enable Cloud Run**: In Google Cloud Console
2. **Setup gcloud CLI**: Download and authenticate
3. **Deploy**:
   ```bash
   gcloud run deploy ai-news-agent \
     --source . \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

#### Features:
- ✅ 2 million requests/month free
- ✅ Pay-per-use model
- ✅ Auto-scaling to zero

---

### 5. 🔵 Streamlit Cloud (Built for Streamlit)

Since your app uses Streamlit, this is a natural choice.

#### Steps:
1. **Visit Streamlit Cloud**: Go to [share.streamlit.io](https://share.streamlit.io)
2. **Sign Up**: Use your GitHub account
3. **Deploy App**:
   - Click "New app"
   - Repository: `ZainulabdeenOfficial/social-news-bot`
   - Branch: `main`
   - Main file path: `web_dashboard.py`
4. **Add Secrets**: Add your API keys in the secrets management

#### Features:
- ✅ Unlimited public apps
- ✅ Built specifically for Streamlit
- ✅ Easy secrets management

---

## 🔧 Environment Variables Setup

For any platform, you'll need these environment variables:

### Required:
```
OPENAI_API_KEY=sk-your-openai-api-key
```

### Optional (for full functionality):
```
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

## 🔑 Getting API Keys

### OpenAI API Key (Required)
1. Visit [platform.openai.com](https://platform.openai.com)
2. Sign up/login
3. Go to API Keys section
4. Create new secret key
5. Copy the key (starts with `sk-`)

### LinkedIn API
1. Visit [LinkedIn Developer Portal](https://developer.linkedin.com)
2. Create an app
3. Get Client ID, Client Secret, and Access Token

### Twitter API
1. Visit [Twitter Developer Portal](https://developer.twitter.com)
2. Create an app
3. Generate API keys and access tokens

### Facebook API
1. Visit [Facebook for Developers](https://developers.facebook.com)
2. Create an app
3. Get access token and page ID

## 🚀 Quick Deploy Commands

### Railway (One-click):
1. Click: [![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/ZainulabdeenOfficial/social-news-bot)

### Render (One-click):
1. Click: [![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/ZainulabdeenOfficial/social-news-bot)

### Heroku (One-click):
1. Click: [![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/ZainulabdeenOfficial/social-news-bot)

## ✅ Post-Deployment Checklist

After deployment:

1. **✅ Access your app** - Visit the provided URL
2. **✅ Configure API keys** - Go to Settings tab in the web dashboard
3. **✅ Test connections** - Use the "Test Connections" feature
4. **✅ Run a test post** - Try posting content immediately
5. **✅ Set up scheduling** - Configure your posting schedule
6. **✅ Monitor logs** - Check for any errors

## 🔍 Troubleshooting

### Common Issues:

#### 1. App not starting
- **Check logs** in your platform's dashboard
- **Verify environment variables** are set correctly
- **Ensure all dependencies** are in requirements.txt

#### 2. API connection errors
- **Verify API keys** are correct and active
- **Check API quotas** - some APIs have usage limits
- **Test individual APIs** using the dashboard

#### 3. Streamlit not loading
- **Check PORT configuration** - ensure `--server.port=$PORT`
- **Verify headless mode** - should be enabled for deployment
- **Check firewall settings** on your platform

#### 4. Memory/timeout issues
- **Optimize memory usage** - consider reducing image generation frequency
- **Increase timeout settings** in platform configuration
- **Use caching** for news data

### Getting Help:

1. **Check platform docs**: Each platform has extensive documentation
2. **Community support**: Join platform-specific Discord/Slack channels
3. **GitHub Issues**: Report bugs in your repository
4. **Platform support**: Contact platform support if needed

## 📊 Monitoring Your Deployed App

### Performance Monitoring:
- **Response times** - Monitor through platform dashboards
- **Error rates** - Set up alerts for failures
- **Resource usage** - Monitor memory and CPU usage
- **API quotas** - Track OpenAI and social media API usage

### Logs Access:
- **Railway**: View logs in dashboard
- **Render**: Real-time logs in dashboard
- **Heroku**: `heroku logs --tail`
- **Google Cloud**: Cloud Logging console

## 🔄 Continuous Deployment

Set up automatic deployments:

1. **Connect GitHub** - Most platforms auto-deploy on push
2. **Branch protection** - Deploy only from main branch
3. **Environment separation** - Use staging environment for testing
4. **Health checks** - Set up monitoring for app health

## 🎯 Production Tips

### Security:
- ✅ Never commit API keys to GitHub
- ✅ Use platform environment variables
- ✅ Enable HTTPS (usually automatic)
- ✅ Set up proper CORS if needed

### Performance:
- ✅ Use caching for news data
- ✅ Optimize image sizes
- ✅ Monitor API rate limits
- ✅ Set up proper error handling

### Reliability:
- ✅ Set up health checks
- ✅ Configure restart policies
- ✅ Monitor resource usage
- ✅ Set up alerts for failures

---

**🎉 Congratulations! Your AI News Agent is now deployed and ready to automate your social media presence!**

## 🔗 Useful Links

- **GitHub Repository**: [https://github.com/ZainulabdeenOfficial/social-news-bot](https://github.com/ZainulabdeenOfficial/social-news-bot)
- **Railway**: [railway.app](https://railway.app)
- **Render**: [render.com](https://render.com)
- **Heroku**: [heroku.com](https://heroku.com)
- **Streamlit Cloud**: [share.streamlit.io](https://share.streamlit.io)
- **OpenAI API**: [platform.openai.com](https://platform.openai.com)

---

**Made with ❤️ by M Zain Ul Abideen**
