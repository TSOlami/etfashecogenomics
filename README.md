# EcoGenomics Suite

A comprehensive platform for environmental and genomic data analysis.

## Project Structure

- **`demo/`** - Original static demo (HTML/CSS/JS)
- **`app/`** - Main Django application (production-ready)

## Quick Start

### Demo Version
```bash
cd demo
python3 -m http.server 8080
# Visit http://localhost:8080
```

### Production Application
```bash
cd app
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
# Visit http://localhost:8000
```

## Features

- **Authentication & User Management** ✅
- **Project Management** ✅
- **File Upload System** 🚧
- **Data Analysis Pipeline** 🚧
- **Visualization Dashboard** 🚧

## Technology Stack

- **Backend**: Django 4.2 + Django REST Framework
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **Frontend**: Django Templates + Tailwind CSS
- **Task Queue**: Celery + Redis (optional)

## Development

The main development happens in the `app/` directory. See `app/README.md` for detailed setup instructions.