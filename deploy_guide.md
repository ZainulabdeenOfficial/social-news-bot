# 🚀 Deployment Guide - AI News Agent

This guide will help you deploy your AI News Agent to various free hosting platforms.

## 📋 Prerequisites

1. **GitHub Account**: For code hosting
2. **API Keys**: OpenAI API key (required), social media API keys (optional)
3. **Python Knowledge**: Basic understanding of Python and command line

## 🎯 Platform Options

### 1. Railway (Recommended - Easiest)

**Pros**: Free tier, easy setup, automatic deployments
**Cons**: Limited free tier hours

#### Setup Steps:

1. **Create Railway Account**
   ```bash
   # Visit https://railway.app and sign up with GitHub
   ```

2. **Install Railway CLI**
   ```bash
   npm install -g @railway/cli
   ```

3. **Login to Railway**
   ```bash
   railway login
   ```

4. **Initialize Project**
   ```bash
   # In your project directory
   railway init
   ```

5. **Set Environment Variables**
   ```bash
   railway variables set OPENAI_API_KEY=your_openai_api_key
   railway variables set LINKEDIN_ACCESS_TOKEN=your_linkedin_token
   railway variables set TWITTER_API_KEY=your_twitter_key
   ```

6. **Deploy**
   ```bash
   railway up
   ```

7. **Start the Service**
   ```bash
   railway service
   ```

### 2. Render (Great Alternative)

**Pros**: Free tier, reliable, good documentation
**Cons**: Free tier has limitations

#### Setup Steps:

1. **Create Render Account**
   - Visit https://render.com
   - Sign up with GitHub

2. **Connect Repository**
   - Click "New +"
   - Select "Web Service"
   - Connect your GitHub repository

3. **Configure Service**
   ```
   Name: ai-news-agent
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: python main.py run
   ```

4. **Set Environment Variables**
   - Go to Environment tab
   - Add your API keys:
     - `OPENAI_API_KEY`
     - `LINKEDIN_ACCESS_TOKEN`
     - `TWITTER_API_KEY`
     - etc.

5. **Deploy**
   - Click "Create Web Service"
   - Wait for build to complete

### 3. Heroku (Classic Choice)

**Pros**: Well-established, good documentation
**Cons**: No free tier anymore

#### Setup Steps:

1. **Install Heroku CLI**
   ```bash
   # Windows
   winget install --id=Heroku.HerokuCLI
   
   # macOS
   brew tap heroku/brew && brew install heroku
   
   # Linux
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create App**
   ```bash
   heroku create your-ai-news-agent
   ```

4. **Set Environment Variables**
   ```bash
   heroku config:set OPENAI_API_KEY=your_openai_api_key
   heroku config:set LINKEDIN_ACCESS_TOKEN=your_linkedin_token
   heroku config:set TWITTER_API_KEY=your_twitter_key
   ```

5. **Deploy**
   ```bash
   git add .
   git commit -m "Initial deployment"
   git push heroku main
   ```

6. **Start Worker**
   ```bash
   heroku ps:scale worker=1
   ```

### 4. Python Anywhere (Free Hosting)

**Pros**: Free, Python-focused, good for beginners
**Cons**: Limited resources, manual setup

#### Setup Steps:

1. **Create Python Anywhere Account**
   - Visit https://www.pythonanywhere.com
   - Sign up for free account

2. **Upload Code**
   - Go to Files tab
   - Upload your project files
   - Or use Git: `git clone your-repo-url`

3. **Install Dependencies**
   ```bash
   # In Python Anywhere bash console
   pip3 install --user -r requirements.txt
   ```

4. **Set Environment Variables**
   - Create `.env` file in your project directory
   - Add your API keys

5. **Create Scheduled Task**
   - Go to Tasks tab
   - Add new scheduled task:
     - Command: `python3 /home/yourusername/your-project/main.py run`
     - Schedule: Daily at 6:00 AM

### 5. Google Cloud Run (Free Tier)

**Pros**: Generous free tier, scalable
**Cons**: More complex setup

#### Setup Steps:

1. **Install Google Cloud CLI**
   ```bash
   # Download from https://cloud.google.com/sdk/docs/install
   ```

2. **Initialize Project**
   ```bash
   gcloud init
   gcloud config set project your-project-id
   ```

3. **Enable APIs**
   ```bash
   gcloud services enable run.googleapis.com
   ```

4. **Create Dockerfile**
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD ["python", "main.py", "run"]
   ```

5. **Deploy**
   ```bash
   gcloud run deploy ai-news-agent \
     --source . \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

## 🔧 Environment Variables Setup

Create a `.env` file in your project root:

```env
# Required
OPENAI_API_KEY=sk-your-openai-api-key-here

# LinkedIn (Optional)
LINKEDIN_CLIENT_ID=your_linkedin_client_id
LINKEDIN_CLIENT_SECRET=your_linkedin_client_secret
LINKEDIN_ACCESS_TOKEN=your_linkedin_access_token

# Twitter (Optional)
TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET=your_twitter_api_secret
TWITTER_ACCESS_TOKEN=your_twitter_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret

# Facebook (Optional)
FACEBOOK_ACCESS_TOKEN=your_facebook_access_token
FACEBOOK_PAGE_ID=your_facebook_page_id

# Database (Optional - for production)
DATABASE_URL=your_database_url
```

## 🧪 Testing Your Deployment

1. **Test News Fetching**
   ```bash
   python main.py fetch-news
   ```

2. **Test Content Generation**
   ```bash
   python main.py test
   ```

3. **Test Manual Posting**
   ```bash
   python main.py post-now --platform linkedin
   ```

4. **Check Logs**
   ```bash
   # View application logs
   tail -f news_agent.log
   ```

## 📊 Monitoring Your Deployment

### Railway
- Dashboard: https://railway.app/dashboard
- Logs: Available in dashboard
- Metrics: Built-in monitoring

### Render
- Dashboard: https://dashboard.render.com
- Logs: Available in service dashboard
- Health checks: Automatic

### Heroku
- Dashboard: https://dashboard.heroku.com
- Logs: `heroku logs --tail`
- Monitoring: `heroku addons:create papertrail`

### Python Anywhere
- Dashboard: Available in account
- Logs: Check task logs
- Monitoring: Manual checking

## 🔒 Security Best Practices

1. **Never commit API keys**
   - Use environment variables
   - Add `.env` to `.gitignore`

2. **Use strong passwords**
   - Generate secure API keys
   - Rotate keys regularly

3. **Monitor usage**
   - Check API usage limits
   - Monitor costs

4. **Backup data**
   - Regular backups of configuration
   - Export important data

## 🚨 Troubleshooting

### Common Issues:

1. **Import Errors**
   ```bash
   # Make sure all dependencies are installed
   pip install -r requirements.txt
   ```

2. **API Key Errors**
   ```bash
   # Check environment variables
   echo $OPENAI_API_KEY
   ```

3. **Permission Errors**
   ```bash
   # Check file permissions
   chmod +x main.py
   ```

4. **Memory Issues**
   ```bash
   # Optimize for limited resources
   # Reduce MAX_POSTS_PER_DAY in config.py
   ```

### Getting Help:

1. **Check Logs**
   ```bash
   tail -f news_agent.log
   ```

2. **Test Locally First**
   ```bash
   python main.py test
   ```

3. **Verify Configuration**
   ```bash
   python main.py status
   ```

## 📈 Scaling Considerations

### Free Tier Limits:
- **Railway**: 500 hours/month
- **Render**: 750 hours/month
- **Heroku**: No free tier
- **Python Anywhere**: Limited CPU/memory

### Optimization Tips:
1. **Reduce posting frequency**
2. **Use efficient image generation**
3. **Cache news data**
4. **Optimize API calls**

## 🎉 Success Checklist

- [ ] Code deployed successfully
- [ ] Environment variables configured
- [ ] News fetching working
- [ ] Content generation working
- [ ] Social media posting working
- [ ] Scheduling working
- [ ] Monitoring set up
- [ ] Logs accessible
- [ ] Error handling working

## 📞 Support

If you encounter issues:

1. **Check the logs** for error messages
2. **Verify API keys** are correct
3. **Test locally** before deploying
4. **Check platform documentation**
5. **Ask in community forums**

---

**Happy Deploying! 🚀**

Your AI News Agent is now ready to automate your social media presence!
