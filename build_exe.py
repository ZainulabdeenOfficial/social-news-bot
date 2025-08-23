#!/usr/bin/env python3
"""
Build Script for AI News Agent Windows Executable
Creates a standalone .exe file that includes all dependencies
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def install_pyinstaller():
    """Install PyInstaller if not already installed"""
    try:
        import PyInstaller
        print("✅ PyInstaller is already installed")
        return True
    except ImportError:
        print("📦 Installing PyInstaller...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("✅ PyInstaller installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install PyInstaller")
            return False

def create_spec_file():
    """Create PyInstaller spec file for the AI News Agent"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('config.py', '.'),
        ('news_fetcher.py', '.'),
        ('content_generator.py', '.'),
        ('image_generator.py', '.'),
        ('social_media_poster.py', '.'),
        ('scheduler.py', '.'),
        ('web_dashboard.py', '.'),
        ('env_template.txt', '.'),
        ('requirements.txt', '.'),
        ('README.md', '.'),
        ('deploy_guide.md', '.'),
        ('Procfile', '.'),
        ('runtime.txt', '.'),
        ('.gitignore', '.'),
    ],
    hiddenimports=[
        'streamlit',
        'openai',
        'requests',
        'beautifulsoup4',
        'python-dotenv',
        'schedule',
        'Pillow',
        'feedparser',
        'selenium',
        'webdriver-manager',
        'flask',
        'gunicorn',
        'pandas',
        'numpy',
        'matplotlib',
        'seaborn',
        'plotly',
        'tweepy',
        'python-linkedin-v2',
        'facebook-sdk',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='AI_News_Agent',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if os.path.exists('icon.ico') else None,
)
'''
    
    with open('ai_news_agent.spec', 'w') as f:
        f.write(spec_content)
    
    print("✅ Created PyInstaller spec file")

def create_launcher_script():
    """Create a launcher script for the web dashboard"""
    launcher_content = '''#!/usr/bin/env python3
"""
AI News Agent Launcher
Starts the web dashboard in a browser
"""

import os
import sys
import subprocess
import webbrowser
import time
import threading
from pathlib import Path

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
            return False
        
        # Start Streamlit
        cmd = [sys.executable, '-m', 'streamlit', 'run', str(dashboard_path), '--server.port', '8501']
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a moment for server to start
        time.sleep(3)
        
        # Open browser
        webbrowser.open('http://localhost:8501')
        
        print("🚀 AI News Agent Dashboard started!")
        print("📱 Open your browser to: http://localhost:8501")
        print("⏹️  Press Ctrl+C to stop the server")
        
        # Keep the process running
        try:
            process.wait()
        except KeyboardInterrupt:
            process.terminate()
            print("\\n🛑 Dashboard stopped")
        
        return True
        
    except Exception as e:
        print(f"❌ Error starting dashboard: {e}")
        return False

if __name__ == "__main__":
    print("🤖 AI News Agent Launcher")
    print("=" * 40)
    start_dashboard()
'''
    
    with open('launcher.py', 'w') as f:
        f.write(launcher_content)
    
    print("✅ Created launcher script")

def create_icon():
    """Create a simple icon file (placeholder)"""
    # This would create a simple icon, but for now we'll skip it
    # You can add your own icon.ico file to the project
    print("ℹ️  Icon creation skipped. Add your own icon.ico file for custom icon.")

def build_executable():
    """Build the executable using PyInstaller"""
    print("🔨 Building executable...")
    
    try:
        # Build with PyInstaller
        cmd = [
            sys.executable, '-m', 'PyInstaller',
            '--onefile',
            '--console',
            '--name=AI_News_Agent',
            '--add-data=config.py;.',
            '--add-data=news_fetcher.py;.',
            '--add-data=content_generator.py;.',
            '--add-data=image_generator.py;.',
            '--add-data=social_media_poster.py;.',
            '--add-data=scheduler.py;.',
            '--add-data=web_dashboard.py;.',
            '--add-data=env_template.txt;.',
            '--add-data=requirements.txt;.',
            '--add-data=README.md;.',
            '--hidden-import=streamlit',
            '--hidden-import=openai',
            '--hidden-import=requests',
            '--hidden-import=beautifulsoup4',
            '--hidden-import=python-dotenv',
            '--hidden-import=schedule',
            '--hidden-import=Pillow',
            '--hidden-import=feedparser',
            '--hidden-import=pandas',
            '--hidden-import=numpy',
            '--hidden-import=plotly',
            '--hidden-import=tweepy',
            'main.py'
        ]
        
        # Add icon if exists
        if os.path.exists('icon.ico'):
            cmd.extend(['--icon=icon.ico'])
        
        subprocess.check_call(cmd)
        
        print("✅ Executable built successfully!")
        print(f"📁 Location: dist/AI_News_Agent.exe")
        
        # Create a simple batch file for easy launching
        batch_content = '''@echo off
echo 🤖 AI News Agent
echo =================
echo.
echo Starting AI News Agent...
echo.
echo This will:
echo 1. Start the web dashboard
echo 2. Open your browser automatically
echo 3. Allow you to configure API keys
echo.
echo Press any key to continue...
pause >nul
start "" "AI_News_Agent.exe"
'''
        
        with open('dist/Start_AI_News_Agent.bat', 'w') as f:
            f.write(batch_content)
        
        print("✅ Created batch launcher: dist/Start_AI_News_Agent.bat")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return False

def create_installer_script():
    """Create an installer script for easy setup"""
    installer_content = '''@echo off
echo 🤖 AI News Agent Installer
echo ==========================
echo.
echo This installer will:
echo 1. Create necessary directories
echo 2. Copy files to Program Files
echo 3. Create desktop shortcut
echo 4. Set up environment
echo.
echo Press any key to continue...
pause >nul

REM Create installation directory
set INSTALL_DIR=C:\\Program Files\\AI News Agent
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

REM Copy files
echo Copying files...
copy "AI_News_Agent.exe" "%INSTALL_DIR%\\"
copy "Start_AI_News_Agent.bat" "%INSTALL_DIR%\\"
copy "env_template.txt" "%INSTALL_DIR%\\"

REM Create desktop shortcut
echo Creating desktop shortcut...
set DESKTOP=%USERPROFILE%\\Desktop
echo @echo off > "%DESKTOP%\\AI News Agent.bat"
echo cd /d "%INSTALL_DIR%" >> "%DESKTOP%\\AI News Agent.bat"
echo start "" "AI_News_Agent.exe" >> "%DESKTOP%\\AI News Agent.bat"

echo.
echo ✅ Installation complete!
echo.
echo You can now:
echo - Double-click "AI News Agent.bat" on your desktop
echo - Or run from: %INSTALL_DIR%
echo.
echo Press any key to exit...
pause >nul
'''
    
    with open('dist/install.bat', 'w') as f:
        f.write(installer_content)
    
    print("✅ Created installer script: dist/install.bat")

def main():
    """Main build function"""
    print("🤖 AI News Agent - Windows Executable Builder")
    print("=" * 50)
    
    # Check if we're on Windows
    if os.name != 'nt':
        print("❌ This script is designed for Windows only!")
        return
    
    # Install PyInstaller
    if not install_pyinstaller():
        return
    
    # Create launcher script
    create_launcher_script()
    
    # Create icon placeholder
    create_icon()
    
    # Build executable
    if not build_executable():
        return
    
    # Create installer
    create_installer_script()
    
    # Final instructions
    print("\n🎉 Build completed successfully!")
    print("\n📁 Files created in 'dist' folder:")
    print("   - AI_News_Agent.exe (Main executable)")
    print("   - Start_AI_News_Agent.bat (Easy launcher)")
    print("   - install.bat (Installer script)")
    print("\n🚀 To use:")
    print("   1. Run 'install.bat' to install to Program Files")
    print("   2. Or double-click 'AI_News_Agent.exe' directly")
    print("   3. The web dashboard will open in your browser")
    print("\n📝 Note: Users will still need to configure API keys")
    print("   through the web dashboard interface")

if __name__ == "__main__":
    main()
