#!/usr/bin/env python3
"""
AI News Agent Setup Script
Helps users get started with the AI News Agent
"""

import os
import sys
from pathlib import Path

def create_env_file():
    """Create .env file from template"""
    template_file = "env_template.txt"
    env_file = ".env"
    
    if os.path.exists(env_file):
        print(f"⚠️  {env_file} already exists!")
        response = input("Do you want to overwrite it? (y/N): ")
        if response.lower() != 'y':
            print("Setup cancelled.")
            return False
    
    if not os.path.exists(template_file):
        print(f"❌ Template file {template_file} not found!")
        return False
    
    try:
        with open(template_file, 'r') as f:
            template_content = f.read()
        
        with open(env_file, 'w') as f:
            f.write(template_content)
        
        print(f"✅ Created {env_file} from template")
        print("📝 Please edit the .env file with your API keys")
        return True
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'streamlit', 'openai', 'requests', 'beautifulsoup4',
        'python-dotenv', 'schedule', 'Pillow'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\nInstall them with:")
        print("pip install -r requirements.txt")
        return False
    else:
        print("✅ All required packages are installed")
        return True

def main():
    """Main setup function"""
    print("🤖 AI News Agent Setup")
    print("=" * 40)
    
    # Check dependencies
    print("\n1. Checking dependencies...")
    if not check_dependencies():
        return
    
    # Create .env file
    print("\n2. Setting up configuration...")
    if not create_env_file():
        return
    
    # Instructions
    print("\n3. Next steps:")
    print("   📝 Edit .env file with your API keys")
    print("   🚀 Start the web dashboard: streamlit run web_dashboard.py")
    print("   ⚙️  Configure settings in the web dashboard")
    print("   🧪 Test the system: python main.py test")
    print("   ▶️  Start the agent: python main.py run")
    
    print("\n📚 For more information, see README.md")
    print("🎉 Setup complete!")

if __name__ == "__main__":
    main()
