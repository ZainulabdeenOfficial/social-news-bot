# 🖥️ Windows Executable Build Guide

This guide explains how to create a standalone Windows executable for the AI News Agent.

## 📋 Prerequisites

### Required Software
- **Python 3.8+**: https://www.python.org/downloads/
- **Windows 10/11**: The build process is Windows-specific
- **Git** (optional): For version control

### Required Python Packages
```bash
pip install -r requirements.txt
pip install pyinstaller
```

## 🔨 Building the Executable

### Method 1: Automated Build (Recommended)

1. Run:
   ```bash
   build_exe.bat
   ```
2. Wait for completion

### Method 2: Manual Build

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```
2. Build the executable:
   ```bash
   pyinstaller --onefile --console --name="AI_News_Agent" exe_launcher.py
   ```

## 📁 Output Files

```
dist/
├── AI_News_Agent.exe
├── build/
└── AI_News_Agent.spec
```

## 🚀 Installing the Executable

### Automated Installer
```bash
install_exe.bat
```

### Manual Installation
- Copy the executable
- Create a shortcut
- Run to start

## 🔧 Troubleshooting Build Issues

Common fixes:
```bash
pip install pyinstaller
pip install -r requirements.txt
```
Also check: permissions, Python version, disk space.

## 📦 Distribution

Include:
```
AI_News_Agent_Package/
├── AI_News_Agent.exe
├── env_template.txt
├── EXECUTABLE_README.md
├── run_ai_agent.bat
└── install_exe.bat
```

## 🔒 Security Considerations
- Consider code signing
- Antiviruses may flag unsigned binaries

## 📝 Notes
- File size: ~50-100MB
- Startup: 10-30s first run
- Memory: ~200-500MB


