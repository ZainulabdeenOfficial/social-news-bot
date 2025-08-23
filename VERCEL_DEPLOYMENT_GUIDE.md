# 🚀 AI News Agent - Vercel Deployment Guide

This guide will help you deploy your AI News Agent to Vercel with step-by-step instructions.

## 📋 Prerequisites

- ✅ GitHub account
- ✅ Vercel account (free)
- ✅ OpenAI API key
- ✅ Social media API keys (optional)

## 🎯 Quick Deploy (Recommended)

### Option 1: One-Click Deploy
1. **Click the Deploy Button**: [![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/ZainulabdeenOfficial/social-news-bot)
2. **Connect GitHub**: Authorize Vercel to access your GitHub account
3. **Configure Project**: 
   - Project Name: `ai-news-agent` (or your preferred name)
   - Framework Preset: `Other`
   - Root Directory: `./` (leave as default)
4. **Deploy**: Click "Deploy" and wait for the build to complete

### Option 2: Manual Deploy
1. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy from your project directory**:
   ```bash
   vercel
   ```

## ⚙️ Environment Variables Setup

After deployment, you need to configure environment variables in Vercel:

### 1. Access Vercel Dashboard
1. Go to [vercel.com/dashboard](https://vercel.com/dashboard)
2. Select your deployed project
3. Go to "Settings" → "Environment Variables"

### 2. Add Required Variables

#### Required (OpenAI):
```
OPENAI_API_KEY=sk-your-openai-api-key-here
```

#### Optional (Social Media):
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

### 3. Redeploy
After adding environment variables, redeploy your project:
```bash
vercel --prod
```

## 🔧 Project Structure

Your Vercel deployment uses this structure:

```
├── api/
│   └── index.py          # Main API endpoint
├── web_dashboard.py      # Streamlit dashboard (for local use)
├── main.py              # CLI application
├── config.py            # Configuration management
├── news_fetcher.py      # News fetching logic
├── content_generator.py # AI content generation
├── image_generator.py   # Image generation
├── social_media_poster.py # Social media posting
├── scheduler.py         # Scheduling logic
├── requirements.txt     # Python dependencies
└── vercel.json         # Vercel configuration
```

## 🌐 Accessing Your Deployed App

After successful deployment, your app will be available at:
- **Production URL**: `https://your-project-name.vercel.app`
- **Preview URLs**: Available for each Git branch/PR

## 📊 Features Available

### ✅ Deployed Features:
- **Dashboard Interface**: Beautiful web interface showing app status
- **Health Check**: `/health` endpoint for monitoring
- **API Status**: `/api/status` endpoint for component status
- **Responsive Design**: Works on desktop and mobile
- **Auto-deployment**: Deploys automatically on GitHub push

### 🔄 Local Development:
- **Streamlit Dashboard**: Run `streamlit run web_dashboard.py` locally
- **CLI Interface**: Run `python main.py` for command-line access
- **Full Functionality**: All features available locally

## 🚀 Advanced Configuration

### Custom Domain
1. Go to Vercel Dashboard → Settings → Domains
2. Add your custom domain
3. Configure DNS records as instructed

### Environment-Specific Variables
Set different variables for different environments:
- **Production**: `vercel env add OPENAI_API_KEY production`
- **Preview**: `vercel env add OPENAI_API_KEY preview`
- **Development**: `vercel env add OPENAI_API_KEY development`

### Build Optimization
The current setup is optimized for Vercel:
- Uses Flask for serverless compatibility
- Minimal dependencies for faster builds
- Efficient routing configuration

## 🔍 Monitoring & Debugging

### Vercel Dashboard
- **Functions**: Monitor serverless function performance
- **Analytics**: Track usage and performance
- **Logs**: View real-time deployment and runtime logs

### Health Checks
- **Endpoint**: `https://your-app.vercel.app/health`
- **Response**: JSON with service status
- **Monitoring**: Use for uptime monitoring services

### API Status
- **Endpoint**: `https://your-app.vercel.app/api/status`
- **Response**: Component status information
- **Usage**: Monitor individual service health

## 🛠️ Troubleshooting

### Common Issues:

#### 1. Build Failures
```bash
# Check build logs in Vercel dashboard
# Common causes:
# - Missing dependencies in requirements.txt
# - Python version incompatibility
# - Import errors
```

#### 2. Environment Variables Not Working
```bash
# Verify variables are set correctly
vercel env ls

# Redeploy after adding variables
vercel --prod
```

#### 3. API Connection Errors
- Check API keys are correct
- Verify API quotas and limits
- Test API endpoints individually

#### 4. Function Timeouts
- Vercel has a 10-second timeout limit
- Optimize code for faster execution
- Consider breaking long operations

### Getting Help:
1. **Vercel Documentation**: [vercel.com/docs](https://vercel.com/docs)
2. **Vercel Support**: Available in dashboard
3. **Community**: Vercel Discord/Forums
4. **GitHub Issues**: Report bugs in your repository

## 🔄 Continuous Deployment

### Automatic Deployments
- **GitHub Integration**: Automatically deploys on push to main branch
- **Preview Deployments**: Creates preview URLs for pull requests
- **Branch Deployments**: Deploy different branches to different URLs

### Deployment Workflow
1. **Push to GitHub**: Triggers automatic deployment
2. **Build Process**: Vercel builds your application
3. **Deployment**: Deploys to production or preview
4. **Verification**: Check deployment status in dashboard

## 📈 Performance Optimization

### Vercel Optimizations:
- **Edge Functions**: Deploy functions closer to users
- **CDN**: Automatic content delivery network
- **Caching**: Intelligent caching strategies
- **Auto-scaling**: Handles traffic spikes automatically

### Best Practices:
- Keep dependencies minimal
- Optimize image sizes
- Use efficient algorithms
- Monitor function execution times

## 🔒 Security Considerations

### Environment Variables:
- ✅ Never commit API keys to GitHub
- ✅ Use Vercel's environment variable system
- ✅ Rotate keys regularly
- ✅ Use least privilege principle

### API Security:
- ✅ Validate all inputs
- ✅ Implement rate limiting
- ✅ Use HTTPS (automatic on Vercel)
- ✅ Monitor for suspicious activity

## 🎉 Success Checklist

After deployment, verify:

- ✅ [ ] App is accessible at Vercel URL
- ✅ [ ] Health check endpoint returns 200
- ✅ [ ] Environment variables are configured
- ✅ [ ] API keys are working
- ✅ [ ] Auto-deployment is enabled
- ✅ [ ] Custom domain is configured (optional)
- ✅ [ ] Monitoring is set up
- ✅ [ ] Documentation is updated

## 🔗 Useful Links

- **Vercel Dashboard**: [vercel.com/dashboard](https://vercel.com/dashboard)
- **Vercel Documentation**: [vercel.com/docs](https://vercel.com/docs)
- **GitHub Repository**: [github.com/ZainulabdeenOfficial/social-news-bot](https://github.com/ZainulabdeenOfficial/social-news-bot)
- **OpenAI API**: [platform.openai.com](https://platform.openai.com)
- **Vercel CLI**: [vercel.com/docs/cli](https://vercel.com/docs/cli)

---

**🎉 Congratulations! Your AI News Agent is now deployed on Vercel and ready to use!**

**Made with ❤️ by M Zain Ul Abideen**
