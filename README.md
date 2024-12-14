# Event Management API

## Overview

Event Management API is a robust Django-based RESTful web service designed for creating, managing, and registering events. The application provides a comprehensive solution for event organizers and participants with advanced features and scalable architecture.

## 🚀 Technologies

- **Backend**: 
  - Python 3.10+
  - Django 5.1
  - Django REST Framework
- **Database**: PostgreSQL
- **Infrastructure**: 
  - Docker
  - docker-compose
- **Authentication**: JWT
- **Documentation**: Swagger/ReDoc

## 📋 Features

- Complete Event CRUD Operations
- User Registration and Authentication
- Event Registration System
- Advanced Search and Filtering
- Email Notifications
- Comprehensive API Documentation
- Containerized Deployment

## 🔧 Prerequisites

- Python 3.10+
- Docker (optional, but recommended)
- pip
- virtualenv

## 💻 Local Development Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Sma1lON/event_management
cd event_management
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# Or for Windows
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Configuration
Create a `.env` file in the project root with the following content:
```env
DEBUG=True
SECRET_KEY=your-secret-key
POSTGRES_DB=events_db
POSTGRES_USER=events_user
POSTGRES_PASSWORD=events_password
DB_HOST=db
DB_PORT=5432
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
```

### 5. Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser
```bash
python manage.py createsuperuser
```

### 7. Run Development Server
```bash
python manage.py runserver
```

## 🐳 Docker Deployment

### Quick Start with Docker
```bash
docker-compose up --build
```

## 🔐 Authentication Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/auth/register/` | POST | User Registration |
| `/api/auth/login/` | POST | User Login |
| `/api/auth/token/` | POST | JWT Token Generation |
| `/api/auth/token/refresh/` | POST | JWT Token Refresh |

## 🔐 Authentication API Endpoints

| Endpoint                        | Method | Description            | Request Body |
|----------------------------------|--------|------------------------|--------------|
| `/api/accounts/register/`        | POST   | Register a new user     | `{ "username": "string", "email": "string", "password": "string", "password2": "string", "first_name": "string", "last_name": "string" }` |
| `/api/accounts/token/`           | POST   | Obtain JWT token       | `{ "username": "string", "password": "string" }` |
| `/api/accounts/token/refresh/`   | POST   | Refresh JWT token      | `{ "refresh": "string" }` |


## 📡 Event API Endpoints

| Endpoint | Method | Description | Authentication |
|----------|--------|-------------|----------------|
| `/api/events/` | GET | List Events | Not Required |
| `/api/events/` | POST | Create Event | Required |
| `/api/events/{id}/` | GET | Event Details | Not Required |
| `/api/events/{id}/` | PUT/PATCH | Update Event | Required (Organizer) |
| `/api/events/{id}/` | DELETE | Delete Event | Required (Organizer) |
| `/api/events/{id}/register/` | POST | Register for Event | Required |
| `/api/events/{id}/unregister/` | DELETE | Unregister from Event | Required |

## 🔍 Filtering and Search

Supported Query Parameters:
- `search`: Search across events
- `start_date`: Filter by start date
- `location`: Filter by event location
- `ordering`: Sort events

Example:
```
/api/events/?search=conference&location=New York&ordering=date
```

## 📄 API Documentation

- **Swagger UI**: `/swagger/`
- **ReDoc**: `/redoc/`


