# 🚀 Quick Deploy to Vercel

## 🎯 One-Click Deployment (Easiest Method)

### Step 1: Deploy to Vercel
Click the button below to deploy your AI News Agent to Vercel:

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/ZainulabdeenOfficial/social-news-bot)

### Step 2: Configure Your Project
1. **Project Name**: Choose a name for your project (e.g., `ai-news-agent`)
2. **Framework Preset**: Select `Other`
3. **Root Directory**: Leave as `./` (default)
4. **Click Deploy**: Wait for the build to complete

### Step 3: Set Environment Variables
After deployment, configure your API keys:

1. Go to your [Vercel Dashboard](https://vercel.com/dashboard)
2. Select your deployed project
3. Go to **Settings** → **Environment Variables**
4. Add the following variables:

#### Required:
```
OPENAI_API_KEY=sk-your-openai-api-key-here
```

#### Optional (for full functionality):
```
LINKEDIN_CLIENT_ID=your_linkedin_client_id
LINKEDIN_CLIENT_SECRET=your_linkedin_client_secret
LINKEDIN_ACCESS_TOKEN=your_linkedin_access_token
TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET=your_twitter_api_secret
TWITTER_ACCESS_TOKEN=your_twitter_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret
FACEBOOK_ACCESS_TOKEN=your_facebook_access_token
FACEBOOK_PAGE_ID=your_facebook_page_id
```

### Step 4: Redeploy
After adding environment variables, redeploy your project:
1. Go to **Deployments** tab
2. Click **Redeploy** on your latest deployment

## 🌐 Access Your App

Your app will be available at:
- **Production URL**: `https://your-project-name.vercel.app`
- **Health Check**: `https://your-project-name.vercel.app/health`
- **API Status**: `https://your-project-name.vercel.app/api/status`

## 🔧 Alternative Deployment Methods

### Method 2: GitHub Integration
1. Push your code to GitHub
2. Connect your GitHub repository to Vercel
3. Vercel will automatically deploy on every push

### Method 3: Manual Upload
1. Download your project as ZIP
2. Upload to Vercel via dashboard
3. Configure environment variables

## 🎉 Success!

Once deployed, you'll have:
- ✅ Beautiful web dashboard
- ✅ Health monitoring endpoints
- ✅ Automatic deployments on code changes
- ✅ Global CDN and SSL
- ✅ 99.9% uptime guarantee

## 📞 Need Help?

- **Documentation**: [VERCEL_DEPLOYMENT_GUIDE.md](VERCEL_DEPLOYMENT_GUIDE.md)
- **Vercel Support**: Available in dashboard
- **GitHub Issues**: Report problems in repository

---

**Made with ❤️ by M Zain Ul Abideen**
