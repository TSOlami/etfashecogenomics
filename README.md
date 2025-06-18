# EcoGenomics Suite

A comprehensive platform for environmental and genomic data analysis.

## Project Structure

- **`demo/`** - Original static demo (HTML/CSS/JS)
- **`app/`** - Main Django application (production-ready)

## Quick Start

### For Windows Users
**Important**: Follow the detailed Windows setup guide first!
```bash
# See SETUP-WINDOWS.md for complete instructions
cd app
python -m venv venv
source venv/Scripts/activate  # Git Bash
pip install -r requirements-windows.txt
```

### Demo Version
```bash
cd demo
python3 -m http.server 8080
# Visit http://localhost:8080
```

### Production Application (Linux/Mac)
```bash
cd app
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
# Visit http://localhost:8000
```

### Production Application (Windows)
```bash
cd app
python -m venv venv
source venv/Scripts/activate  # Git Bash
pip install -r requirements-windows.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
# Visit http://localhost:8000
```

## Features

- **Authentication & User Management** ✅
- **Dashboard with Charts & Metrics** ✅
- **Analytics with Tabs** ✅
- **Data Management** ✅
- **Reports & Exports** ✅
- **Responsive Design** ✅

## Technology Stack

- **Backend**: Django 4.2 + Django REST Framework
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **Frontend**: Django Templates + Tailwind CSS
- **Charts**: Chart.js
- **Task Queue**: Celery + Redis (optional)

## Platform-Specific Setup

- **Windows**: See `SETUP-WINDOWS.md` for detailed instructions
- **Linux/Mac**: Use standard `requirements.txt`

## Development

The main development happens in the `app/` directory. The application uses SQLite by default for development, so no additional database setup is required.

## Demo Features Implemented

All features from the original demo have been faithfully recreated:

1. **Dashboard**: Environmental monitoring charts, species diversity, sample processing status, recent samples table, analysis results, and quick actions
2. **Analytics**: Four-tab interface with diversity analysis, taxonomic composition, environmental correlation, and phylogenetic analysis
3. **Data Management**: File overview cards, data files table with filtering and search
4. **Reports**: Report templates and recent reports table
5. **Authentication**: Login and registration with the same styling as demo

## Troubleshooting

### Windows Issues
- Use `requirements-windows.txt` instead of `requirements.txt`
- Make sure virtual environment is activated
- Skip PostgreSQL packages for development

### General Issues
- Ensure Python 3.8+ is installed
- Always activate virtual environment before installing packages
- Check that you're in the correct directory (`app/`)