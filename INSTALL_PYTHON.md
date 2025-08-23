# 🐍 Python Installation Guide for Windows

This guide will help you install Python on Windows so you can build the AI News Agent executable.

## 📥 Method 1: Official Python Website (Recommended)

### Step 1: Download Python
1. Go to [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Click the big yellow "Download Python" button
3. Choose Python 3.11 or higher

### Step 2: Install Python
1. **Run the installer** you downloaded
2. **IMPORTANT**: Check ✅ "Add Python to PATH"
3. Click "Install Now"
4. Wait for installation to complete
5. Click "Close"

### Step 3: Verify Installation
1. Open Command Prompt or PowerShell
2. Type: `python --version`
3. You should see something like: `Python 3.11.x`

## 🏪 Method 2: Microsoft Store (Alternative)

1. Open Microsoft Store
2. Search for "Python"
3. Install "Python 3.11" or higher
4. Wait for installation to complete

## 🔧 Method 3: Manual PATH Setup

If Python is installed but not in PATH:

1. Find your Python installation (usually `C:\Users\YourName\AppData\Local\Programs\Python\Python311\`)
2. Open System Properties → Advanced → Environment Variables
3. Edit the "Path" variable
4. Add these two paths:
   - `C:\Users\YourName\AppData\Local\Programs\Python\Python311\`
   - `C:\Users\YourName\AppData\Local\Programs\Python\Python311\Scripts\`

## ✅ Verification

After installation, test these commands:

```bash
# Check Python
python --version

# Check pip
pip --version

# Check if you can install packages
pip install requests
```

## 🚀 Next Steps

Once Python is installed:

1. **Restart** your Command Prompt/PowerShell
2. **Navigate** to your AI News Agent folder
3. **Run**: `build_exe.bat`

## 🔧 Troubleshooting

### "Python is not recognized"
- Make sure you checked "Add Python to PATH" during installation
- Restart Command Prompt after installation
- Try using `py` instead of `python`

### "pip is not recognized"
- Python may not have been installed with pip
- Try: `python -m ensurepip --upgrade`

### Permission Errors
- Run Command Prompt as Administrator
- Check if antivirus is blocking Python

### Still Having Issues?
1. Uninstall Python completely
2. Restart your computer
3. Install Python again with "Add to PATH" checked
4. Try the build process again

## 📞 Need Help?

If you're still having issues:
1. Check the Python installation guide on python.org
2. Make sure you're using Windows 10 or 11
3. Try installing Python 3.11 specifically

---

**Happy Coding! 🐍✨**
