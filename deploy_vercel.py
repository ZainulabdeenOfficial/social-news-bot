#!/usr/bin/env python3
"""
AI News Agent - Vercel Deployment Script

This script helps you deploy your AI News Agent to Vercel with ease.
"""

import os
import sys
import subprocess
import json
import webbrowser
from pathlib import Path

def print_banner():
    """Print the deployment banner"""
    print("""
🤖 AI News Agent - Vercel Deployment
====================================

This script will help you deploy your AI News Agent to Vercel.
    """)

def check_prerequisites():
    """Check if all prerequisites are met"""
    print("🔍 Checking prerequisites...")
    
    # Check if we're in the right directory
    required_files = ['vercel.json', 'requirements.txt', 'api/index.py']
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        return False
    
    print("✅ All required files found")
    return True

def check_vercel_cli():
    """Check if Vercel CLI is installed"""
    try:
        result = subprocess.run(['vercel', '--version'], 
                              capture_output=True, text=True, check=True)
        print(f"✅ Vercel CLI found: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Vercel CLI not found")
        return False

def install_vercel_cli():
    """Install Vercel CLI"""
    print("📦 Installing Vercel CLI...")
    try:
        subprocess.run(['npm', 'install', '-g', 'vercel'], check=True)
        print("✅ Vercel CLI installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install Vercel CLI: {e}")
        return False

def login_to_vercel():
    """Login to Vercel"""
    print("🔐 Logging in to Vercel...")
    try:
        subprocess.run(['vercel', 'login'], check=True)
        print("✅ Successfully logged in to Vercel")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to login to Vercel: {e}")
        return False

def deploy_to_vercel():
    """Deploy to Vercel"""
    print("🚀 Deploying to Vercel...")
    try:
        # Deploy to production
        result = subprocess.run(['vercel', '--prod'], 
                              capture_output=True, text=True, check=True)
        print("✅ Deployment successful!")
        
        # Extract the deployment URL
        output = result.stdout
        if 'https://' in output:
            url_start = output.find('https://')
            url_end = output.find('\n', url_start)
            if url_end == -1:
                url_end = len(output)
            deployment_url = output[url_start:url_end].strip()
            print(f"🌐 Your app is live at: {deployment_url}")
            return deployment_url
        
        return None
    except subprocess.CalledProcessError as e:
        print(f"❌ Deployment failed: {e}")
        print(f"Error output: {e.stderr}")
        return None

def setup_environment_variables():
    """Guide user through environment variable setup"""
    print("""
🔧 Environment Variables Setup
==============================

After deployment, you need to set up environment variables in Vercel:

1. Go to your Vercel dashboard: https://vercel.com/dashboard
2. Select your deployed project
3. Go to Settings → Environment Variables
4. Add the following variables:

Required:
- OPENAI_API_KEY=sk-your-openai-api-key-here

Optional (for full functionality):
- LINKEDIN_CLIENT_ID=your_linkedin_client_id
- LINKEDIN_CLIENT_SECRET=your_linkedin_client_secret
- LINKEDIN_ACCESS_TOKEN=your_linkedin_access_token
- TWITTER_API_KEY=your_twitter_api_key
- TWITTER_API_SECRET=your_twitter_api_secret
- TWITTER_ACCESS_TOKEN=your_twitter_access_token
- TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret
- FACEBOOK_ACCESS_TOKEN=your_facebook_access_token
- FACEBOOK_PAGE_ID=your_facebook_page_id

5. After adding variables, redeploy: vercel --prod
    """)

def open_dashboard(url):
    """Open the deployment URL in browser"""
    if url:
        print(f"🌐 Opening dashboard: {url}")
        try:
            webbrowser.open(url)
        except Exception as e:
            print(f"⚠️ Could not open browser automatically: {e}")
            print(f"Please manually visit: {url}")

def main():
    """Main deployment function"""
    print_banner()
    
    # Check prerequisites
    if not check_prerequisites():
        print("❌ Prerequisites not met. Please ensure all required files are present.")
        return False
    
    # Check Vercel CLI
    if not check_vercel_cli():
        print("📦 Vercel CLI not found. Installing...")
        if not install_vercel_cli():
            print("❌ Failed to install Vercel CLI. Please install manually:")
            print("   npm install -g vercel")
            return False
    
    # Login to Vercel
    if not login_to_vercel():
        print("❌ Failed to login to Vercel")
        return False
    
    # Deploy
    deployment_url = deploy_to_vercel()
    if not deployment_url:
        print("❌ Deployment failed")
        return False
    
    # Setup instructions
    setup_environment_variables()
    
    # Open dashboard
    open_dashboard(deployment_url)
    
    print("""
🎉 Deployment Complete!
======================

Your AI News Agent has been successfully deployed to Vercel!

Next steps:
1. Configure environment variables in Vercel dashboard
2. Test your deployment
3. Set up monitoring and alerts
4. Configure custom domain (optional)

For detailed instructions, see: VERCEL_DEPLOYMENT_GUIDE.md
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
