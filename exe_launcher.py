#!/usr/bin/env python3
"""
AI News Agent - Windows Executable Launcher
This script launches the web dashboard and can be converted to .exe
"""

import os
import sys
import subprocess
import webbrowser
import time
import threading
from pathlib import Path

def check_dependencies():
    """Check if required packages are installed"""
    # Skip dependency check if running as executable
    if getattr(sys, 'frozen', False):
        print("✅ Running as executable - dependencies included")
        return True
    
    required_packages = [
        ('streamlit', 'streamlit'),
        ('openai', 'openai'),
        ('requests', 'requests'),
        ('beautifulsoup4', 'bs4'),
        ('python-dotenv', 'dotenv'),
        ('schedule', 'schedule'),
        ('Pillow', 'PIL'),
        ('feedparser', 'feedparser'),
        ('pandas', 'pandas'),
        ('numpy', 'numpy'),
        ('plotly', 'plotly'),
        ('tweepy', 'tweepy')
    ]
    
    missing_packages = []
    
    for package_name, import_name in required_packages:
        try:
            __import__(import_name)
        except ImportError:
            missing_packages.append(package_name)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n⚠️  These packages are required for the AI News Agent to run.")
        print("If you are running the .exe file, you must install these dependencies on your system before running the executable.")
        print("\nTo install all required packages, open a command prompt in this folder and run:")
        print("pip install -r requirements.txt")
        print("\nAfter installing, try running the .exe file again.")
        return False
    
    return True

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_file = Path('.env')
    template_file = Path('env_template.txt')
    
    if not env_file.exists() and template_file.exists():
        try:
            with open(template_file, 'r') as f:
                template_content = f.read()
            
            with open(env_file, 'w') as f:
                f.write(template_content)
            
            print("✅ Created .env file from template")
            return True
        except Exception as e:
            print(f"❌ Error creating .env file: {e}")
            return False
    
    return True

def start_dashboard():
    """Start the Streamlit dashboard"""
    try:
        # Check if we're running from exe
        if getattr(sys, 'frozen', False):
            # Running as exe
            base_path = Path(sys._MEIPASS)
            dashboard_path = base_path / 'web_dashboard.py'
        else:
            # Running as script
            dashboard_path = Path('web_dashboard.py')
        
        if not dashboard_path.exists():
            print("❌ web_dashboard.py not found!")
            print("Please make sure all files are in the same directory.")
            return False
        
        print("🚀 Starting AI News Agent Dashboard...")
        print("📱 This will open in your web browser")
        print("⏳ Please wait...")
        
        # Start Streamlit
        cmd = [
            sys.executable, '-m', 'streamlit', 'run', 
            str(dashboard_path), 
            '--server.port', '8501',
            '--server.headless', 'true',
            '--browser.gatherUsageStats', 'false'
        ]
        
        process = subprocess.Popen(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        )
        
        # Wait a moment for server to start
        time.sleep(5)
        
        # Open browser
        try:
            webbrowser.open('http://localhost:8501')
            print("✅ Dashboard opened in browser!")
        except Exception as e:
            print(f"⚠️  Could not open browser automatically: {e}")
            print("Please open: http://localhost:8501")
        
        print("\n🎉 AI News Agent is running!")
        print("📊 Dashboard: http://localhost:8501")
        print("⚙️  Go to Settings tab to configure API keys")
        print("⏹️  Close this window to stop the server")
        
        # Keep the process running
        try:
            process.wait()
        except KeyboardInterrupt:
            process.terminate()
            print("\n🛑 Dashboard stopped")
        
        return True
        
    except Exception as e:
        print(f"❌ Error starting dashboard: {e}")
        return False

def main():
    """Main launcher function"""
    print("🤖 AI News Agent")
    print("=" * 40)
    print()
    
    # Check dependencies
    print("🔍 Checking dependencies...")
    if not check_dependencies():
        input("\nPress Enter to exit...")
        return
    
    # Create .env file if needed
    print("📝 Setting up configuration...")
    create_env_file()
    
    # Start dashboard
    print("🚀 Launching dashboard...")
    success = start_dashboard()
    
    if not success:
        print("\n❌ Failed to start dashboard")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
