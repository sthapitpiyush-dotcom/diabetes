# Setup Instructions

## Python Installation Required

Python is not currently installed on your system. Please follow these steps:

### Step 1: Install Python

1. **Download Python 3.8 or higher:**
   - Visit: https://www.python.org/downloads/
   - Download the latest Python 3.x version for Windows

2. **During Installation:**
   - ✅ **IMPORTANT:** Check the box "Add Python to PATH"
   - Click "Install Now"

3. **Verify Installation:**
   - Open a new PowerShell/Command Prompt window
   - Run: `python --version`
   - You should see something like: `Python 3.x.x`

### Step 2: Install Dependencies

Open PowerShell/Command Prompt in this directory and run:

```bash
python -m pip install -r requirements.txt
```

### Step 3: Run the Application

**Option A: Run the Web UI (Recommended)**
```bash
python -m streamlit run app.py
```

**Option B: Run the Python Script**
```bash
python diabetes_prediction.py
```

**Option C: Use the Batch Files**
- Double-click `run_app.bat` to run the web UI
- Double-click `run_script.bat` to run the script

## Troubleshooting

### If "python" command is not recognized:
1. Make sure Python was added to PATH during installation
2. Restart your terminal/PowerShell after installing Python
3. Try using the full path to Python (usually in `C:\Users\YourName\AppData\Local\Programs\Python\`)

### If pip is not found:
- Try: `python -m ensurepip --upgrade`
- Or: `python -m pip install --upgrade pip`

## Need Help?

If you encounter any issues, make sure:
- Python 3.8+ is installed
- Python is added to your system PATH
- All dependencies are installed successfully

