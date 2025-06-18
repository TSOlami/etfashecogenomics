# EcoGenomics Suite - Windows Setup Guide

This guide provides step-by-step instructions for setting up the EcoGenomics Suite on Windows.

## Prerequisites

1. **Python 3.8+** - Download from [python.org](https://www.python.org/downloads/)
2. **Git** - Download from [git-scm.com](https://git-scm.com/download/win)
3. **Git Bash or PowerShell** - For running commands

## Step-by-Step Setup

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd ecogenomics-suite
```

### 2. Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment (Git Bash)
source venv/Scripts/activate

# OR activate in PowerShell
venv\Scripts\Activate.ps1

# OR activate in Command Prompt
venv\Scripts\activate.bat
```

**Important**: Always activate your virtual environment before installing packages!

### 3. Install Dependencies (Windows-Specific)
```bash
# Make sure you're in the app directory
cd app

# Upgrade pip first
pip install --upgrade pip

# Install Windows-compatible requirements
pip install -r requirements-windows.txt
```

### 4. Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your preferred text editor
# The default SQLite settings should work fine for development
```

### 5. Database Setup
```bash
# Create database tables
python manage.py makemigrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser
```

### 6. Run the Development Server
```bash
python manage.py runserver
```

Visit `http://localhost:8000` in your browser.

## Troubleshooting Windows Issues

### Issue 1: Pillow Installation Fails
**Error**: `Getting requirements to build wheel did not run successfully`

**Solution**: Use a more flexible Pillow version that installs pre-built wheels:
```bash
pip install Pillow>=9.0.0
```

### Issue 2: psycopg2-binary Compilation Errors
**Error**: `Cannot open include file: 'io.h'`

**Solution**: Skip PostgreSQL for development and use SQLite instead:
```bash
# Don't install psycopg2-binary on Windows unless you have PostgreSQL dev tools
# The app is configured to use SQLite by default
```

### Issue 3: Visual Studio Build Tools Missing
If you encounter C++ compilation errors:

1. Install [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
2. OR use pre-compiled packages from the Windows requirements file

### Issue 4: Virtual Environment Not Activating
Make sure you're using the correct activation command for your shell:

- **Git Bash**: `source venv/Scripts/activate`
- **PowerShell**: `venv\Scripts\Activate.ps1`
- **Command Prompt**: `venv\Scripts\activate.bat`

## Alternative Setup (If Issues Persist)

If you continue having dependency issues, try this minimal setup:

```bash
# Create fresh virtual environment
python -m venv venv-clean
source venv-clean/Scripts/activate

# Install core packages one by one
pip install Django==4.2.7
pip install djangorestframework==3.14.0
pip install django-cors-headers==4.3.1
pip install python-decouple==3.8
pip install django-extensions==3.2.3

# Try Pillow without specific version
pip install Pillow

# Skip optional packages for now
```

## What's Different in Windows Requirements

The `requirements-windows.txt` file excludes problematic packages:

- ❌ `psycopg2-binary` - Requires PostgreSQL dev libraries
- ❌ `celery` + `redis` - Optional for basic functionality
- ✅ `Pillow>=9.0.0` - More flexible version range
- ✅ All core Django packages - Work perfectly on Windows

## Next Steps

Once the server is running:

1. Visit `http://localhost:8000/admin` to access Django admin
2. Visit `http://localhost:8000` for the main application
3. Create user accounts and start exploring!

## Getting Help

If you encounter issues:

1. Make sure your virtual environment is activated
2. Check that you're in the `app/` directory
3. Try the alternative minimal setup above
4. Check the main `README.md` for additional troubleshooting