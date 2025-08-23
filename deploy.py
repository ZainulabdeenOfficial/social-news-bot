#!/usr/bin/env python3
"""
AI News Agent - Universal Deployment Script

This script helps you deploy your AI News Agent to your preferred platform.
"""

import os
import sys
import webbrowser
import subprocess
from pathlib import Path

def print_banner():
    """Print the deployment banner"""
    print("""
🤖 AI News Agent - Universal Deployment
=======================================

Choose your preferred deployment platform:
    """)

def show_platform_options():
    """Show available platform options"""
    print("""
🎯 Available Platforms:

1. 🟣 Vercel (Recommended - Fastest)
   - ⚡ Lightning fast deployments
   - 🌍 Global CDN
   - 🔄 Automatic deployments
   - 📱 Serverless functions
   - 🆓 Generous free tier

2. 🚆 Railway (Easiest)
   - 🎯 One-click deployment
   - 🔧 Easy environment variable management
   - 📊 Built-in monitoring
   - 🆓 500 hours/month free
   - 🔄 GitHub integration

3. 🎨 Render (Most Reliable)
   - 🛡️ DDoS protection
   - 🔒 Automatic SSL
   - 📈 Auto-scaling
   - 🆓 750 hours/month free
   - 🌐 Custom domains

4. 🔵 Heroku (Classic)
   - 🏛️ Established platform
   - 🔧 Extensive add-ons
   - 📊 Advanced monitoring
   - 🆓 550-1000 hours/month free
   - 🛠️ CLI tools

5. 📖 View Documentation
   - Detailed deployment guides
   - Platform comparisons
   - Troubleshooting tips

6. 🚪 Exit
    """)

def check_prerequisites():
    """Check if all prerequisites are met"""
    print("🔍 Checking prerequisites...")
    
    # Check if we're in the right directory
    required_files = ['requirements.txt', 'web_dashboard.py', 'main.py']
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        return False
    
    print("✅ All required files found")
    return True

def deploy_vercel():
    """Deploy to Vercel"""
    print("🟣 Deploying to Vercel...")
    print("Opening Vercel deployment page...")
    
    vercel_url = "https://vercel.com/new/clone?repository-url=https://github.com/ZainulabdeenOfficial/social-news-bot"
    webbrowser.open(vercel_url)
    
    print("""
📋 Vercel Deployment Steps:
1. Click "Deploy" in the opened browser
2. Connect your GitHub account
3. Configure project settings:
   - Project Name: ai-news-agent
   - Framework Preset: Other
   - Root Directory: ./
4. Click "Deploy"
5. Add environment variables in Vercel dashboard
6. Redeploy to apply changes

For detailed instructions, see: VERCEL_DEPLOYMENT_GUIDE.md
    """)

def deploy_railway():
    """Deploy to Railway"""
    print("🚆 Deploying to Railway...")
    print("Opening Railway deployment page...")
    
    railway_url = "https://railway.app/new/template?template=https://github.com/ZainulabdeenOfficial/social-news-bot"
    webbrowser.open(railway_url)
    
    print("""
📋 Railway Deployment Steps:
1. Click "Deploy" in the opened browser
2. Connect your GitHub account
3. Railway will automatically detect configuration
4. Click "Deploy"
5. Add environment variables in Railway dashboard
6. Your app will be live automatically

For detailed instructions, see: MULTI_PLATFORM_DEPLOYMENT.md
    """)

def deploy_render():
    """Deploy to Render"""
    print("🎨 Deploying to Render...")
    print("Opening Render deployment page...")
    
    render_url = "https://render.com/deploy?repo=https://github.com/ZainulabdeenOfficial/social-news-bot"
    webbrowser.open(render_url)
    
    print("""
📋 Render Deployment Steps:
1. Click "Deploy" in the opened browser
2. Connect your GitHub account
3. Configure service:
   - Name: ai-news-agent
   - Environment: Python 3
   - Build Command: pip install -r requirements.txt
   - Start Command: streamlit run web_dashboard.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true --server.enableCORS=false --server.enableXsrfProtection=false
4. Click "Create Web Service"
5. Add environment variables in Render dashboard

For detailed instructions, see: MULTI_PLATFORM_DEPLOYMENT.md
    """)

def deploy_heroku():
    """Deploy to Heroku"""
    print("🔵 Deploying to Heroku...")
    print("Opening Heroku deployment page...")
    
    heroku_url = "https://heroku.com/deploy?template=https://github.com/ZainulabdeenOfficial/social-news-bot"
    webbrowser.open(heroku_url)
    
    print("""
📋 Heroku Deployment Steps:
1. Click "Deploy to Heroku" in the opened browser
2. Connect your GitHub account
3. Configure app:
   - App name: your-ai-news-agent
   - Region: Choose closest to you
4. Click "Deploy app"
5. Add environment variables in Heroku dashboard
6. Your app will be live automatically

For detailed instructions, see: MULTI_PLATFORM_DEPLOYMENT.md
    """)

def show_documentation():
    """Show documentation options"""
    print("""
📖 Documentation Options:

1. Multi-Platform Deployment Guide (MULTI_PLATFORM_DEPLOYMENT.md)
   - Complete guide for all platforms
   - Platform comparison table
   - Troubleshooting tips

2. Vercel Deployment Guide (VERCEL_DEPLOYMENT_GUIDE.md)
   - Detailed Vercel-specific instructions
   - Environment variable setup
   - Advanced configuration

3. Quick Deploy Guide (QUICK_DEPLOY.md)
   - Simple step-by-step instructions
   - One-click deployment options
    """)
    
    choice = input("Enter your choice (1-3) or press Enter to go back: ").strip()
    
    if choice == "1":
        if os.path.exists("MULTI_PLATFORM_DEPLOYMENT.md"):
            print("Opening Multi-Platform Deployment Guide...")
            webbrowser.open("file://" + os.path.abspath("MULTI_PLATFORM_DEPLOYMENT.md"))
        else:
            print("❌ Documentation file not found")
    elif choice == "2":
        if os.path.exists("VERCEL_DEPLOYMENT_GUIDE.md"):
            print("Opening Vercel Deployment Guide...")
            webbrowser.open("file://" + os.path.abspath("VERCEL_DEPLOYMENT_GUIDE.md"))
        else:
            print("❌ Documentation file not found")
    elif choice == "3":
        if os.path.exists("QUICK_DEPLOY.md"):
            print("Opening Quick Deploy Guide...")
            webbrowser.open("file://" + os.path.abspath("QUICK_DEPLOY.md"))
        else:
            print("❌ Documentation file not found")

def main():
    """Main deployment function"""
    print_banner()
    
    # Check prerequisites
    if not check_prerequisites():
        print("❌ Prerequisites not met. Please ensure all required files are present.")
        return False
    
    while True:
        show_platform_options()
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == "1":
            deploy_vercel()
            break
        elif choice == "2":
            deploy_railway()
            break
        elif choice == "3":
            deploy_render()
            break
        elif choice == "4":
            deploy_heroku()
            break
        elif choice == "5":
            show_documentation()
        elif choice == "6":
            print("👋 Goodbye!")
            return True
        else:
            print("❌ Invalid choice. Please enter a number between 1-6.")
    
    print("""
🎉 Deployment Initiated!

Next steps:
1. Complete the deployment process in your browser
2. Add your OpenAI API key in the platform dashboard
3. Add other API keys for full functionality
4. Test your deployment
5. Set up monitoring and alerts

For help and support:
- Documentation: MULTI_PLATFORM_DEPLOYMENT.md
- GitHub Issues: https://github.com/ZainulabdeenOfficial/social-news-bot/issues
- Platform Support: Available in respective dashboards

Happy deploying! 🚀
    """)
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n👋 Deployment cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
