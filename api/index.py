import os
import sys
import subprocess
import threading
import time
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from flask import Flask, render_template_string, redirect

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__)

# HTML template for the dashboard
DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>AI News Agent Dashboard</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        .header h1 {
            color: #333;
            font-size: 2.5rem;
            margin-bottom: 10px;
        }
        .header p {
            color: #666;
            font-size: 1.1rem;
        }
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .feature-card {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }
        .feature-card h3 {
            color: #333;
            margin-top: 0;
        }
        .feature-card p {
            color: #666;
            line-height: 1.6;
        }
        .deployment-info {
            background: #e3f2fd;
            padding: 20px;
            border-radius: 8px;
            margin-top: 20px;
        }
        .deployment-info h3 {
            color: #1976d2;
            margin-top: 0;
        }
        .deployment-info ul {
            color: #333;
            line-height: 1.8;
        }
        .status {
            display: inline-block;
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 0.9rem;
            font-weight: bold;
        }
        .status.success {
            background: #d4edda;
            color: #155724;
        }
        .status.warning {
            background: #fff3cd;
            color: #856404;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 AI News Agent</h1>
            <p>Automated Tech News Fetcher and Social Media Poster</p>
        </div>
        
        <div class="features">
            <div class="feature-card">
                <h3>📰 News Fetching</h3>
                <p>Automatically fetches the latest tech news from multiple sources including TechCrunch, The Verge, and more.</p>
            </div>
            <div class="feature-card">
                <h3>🤖 AI Content Generation</h3>
                <p>Uses OpenAI to generate engaging social media posts with professional images for each news article.</p>
            </div>
            <div class="feature-card">
                <h3>📱 Social Media Posting</h3>
                <p>Automatically posts to LinkedIn, Twitter, and other social media platforms at optimal times.</p>
            </div>
            <div class="feature-card">
                <h3>⏰ Smart Scheduling</h3>
                <p>Intelligent scheduling system that posts content at the best times for maximum engagement.</p>
            </div>
        </div>
        
        <div class="deployment-info">
            <h3>🚀 Deployment Status</h3>
            <p><span class="status success">✅ Successfully Deployed on Vercel</span></p>
            <ul>
                <li><strong>Platform:</strong> Vercel Serverless Functions</li>
                <li><strong>Status:</strong> <span class="status success">Active</span></li>
                <li><strong>Auto-deploy:</strong> Enabled (deploys on GitHub push)</li>
                <li><strong>Environment:</strong> Production</li>
            </ul>
        </div>
        
        <div class="deployment-info">
            <h3>🔧 Setup Instructions</h3>
            <p><span class="status warning">⚠️ Configuration Required</span></p>
            <ul>
                <li>Add your <strong>OpenAI API Key</strong> in Vercel environment variables</li>
                <li>Configure social media API keys (LinkedIn, Twitter, Facebook)</li>
                <li>Set up posting schedules in the dashboard</li>
                <li>Test the connections before enabling auto-posting</li>
            </ul>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def dashboard():
    """Main dashboard page"""
    return render_template_string(DASHBOARD_HTML)

@app.route('/health')
def health_check():
    """Health check endpoint for Vercel"""
    return {
        'status': 'healthy',
        'service': 'AI News Agent',
        'version': '1.0.0',
        'deployment': 'vercel'
    }

@app.route('/api/status')
def api_status():
    """API status endpoint"""
    return {
        'status': 'operational',
        'components': {
            'news_fetcher': 'ready',
            'content_generator': 'ready',
            'image_generator': 'ready',
            'social_poster': 'ready',
            'scheduler': 'ready'
        }
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
