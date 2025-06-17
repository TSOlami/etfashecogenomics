# EcoGenomics Suite - Production Application

This is the main application directory for the EcoGenomics Suite platform.

## Architecture Overview

- **Backend**: Django 4.2 + Django REST Framework
- **Database**: SQLite (development) / PostgreSQL (production)
- **Task Queue**: Celery + Redis (optional)
- **File Storage**: Django storage backends
- **API**: RESTful with Django REST Framework
- **Frontend**: Django templates with Tailwind CSS

## Development Setup

1. **Install Dependencies**
   ```bash
   cd app
   pip install -r requirements.txt
   ```

2. **Environment Setup**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

3. **Database Setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

4. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `GET /api/auth/profile/` - Get user profile
- `PUT /api/auth/profile/update/` - Update profile
- `POST /api/auth/password/change/` - Change password

### Core Features
- Project management
- File upload and processing
- Analysis job tracking
- Results visualization

## Features Implemented

✅ **Authentication & User Management**
- Custom user model with roles
- Registration and login
- Profile management
- Security features (login tracking, IP logging)

🚧 **Next Features to Implement**
- File upload system
- Data processing pipeline
- Analysis algorithms
- Results visualization
- Dashboard analytics

## Project Structure

```
app/
├── accounts/          # User management
├── core/             # Core functionality
├── analytics/        # Data analysis
├── templates/        # HTML templates
├── static/          # Static files
├── media/           # Uploaded files
└── manage.py        # Django management
```