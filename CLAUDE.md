# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Django-based backend API for a goal-tracking application called "goal-star-backend". The project uses Django Ninja for API endpoints and integrates with Clerk for authentication. The application is deployed on Railway.

## Architecture

### Core Structure
- **service/**: Main Django project configuration
  - `settings.py`: Django settings with environment-based configuration
  - `urls.py`: Root URL configuration
  - `api.py`: Central API instance using Django Ninja
- **user/**: User management app with custom User model extending AbstractUser
- **goal/**: Goal management app with Goal model and CRUD operations
- **utils/**: Shared utilities including generic API response schemas

### Key Components
- Custom User model (`user.User`) extends Django's AbstractUser
- Goal model with title, description, deadline, and friendEmail fields
- Authentication via Clerk integration with custom `AuthBearer` class
- API responses use generic schemas (`ListSchema`, `ObjectSchema`, `DetailSchema`)

### Authentication Flow
The app uses Clerk for authentication:
1. `user.clerk.is_signed_in()` validates requests using Clerk SDK
2. `AuthBearer` class handles authentication for protected endpoints
3. User onboarding creates Django user linked to Clerk user ID

## Development Commands

### Environment Setup
- Uses `uv` for dependency management (see `pyproject.toml`)
- Requires Python >=3.13
- Environment variables loaded via `django-environ` from `.env` file

### Common Commands (via Makefile)
```bash
make dev        # Run development server (includes check and migrate)
make check      # Run Django system checks
make migrate    # Create and apply database migrations
make dump       # Export user data to fixtures
make load       # Load data from fixtures
```

### Direct Django Commands
```bash
python manage.py runserver     # Start development server
python manage.py makemigrations # Create migration files
python manage.py migrate       # Apply migrations
python manage.py check         # Run system checks
```

### Deployment
- Railway deployment configured via `railway.json`
- Production command: `python manage.py migrate && python manage.py collectstatic --noinput && gunicorn service.wsgi`
- Uses Gunicorn with WhiteNoise for static file serving

## Database

- Uses PostgreSQL in production (via `env.db()`)
- SQLite for development (db.sqlite3)
- Custom User model: `AUTH_USER_MODEL = "user.User"`

## API Structure

All API endpoints are prefixed with `/api/` and organized by app:
- `/api/user/` - User management (onboarding)
- `/api/goal/` - Goal CRUD operations (authenticated)

## Environment Variables

Required environment variables:
- `SECRET_KEY`: Django secret key
- `DEBUG`: Debug mode boolean
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `DATABASE_URL`: Database connection string
- `CORS_ALLOWED_ORIGINS`: CORS allowed origins
- `CSRF_TRUSTED_ORIGINS`: CSRF trusted origins
- `PUBLIC_CLERK_PUBLISHABLE_KEY`: Clerk publishable key
- `CLERK_SECRET_KEY`: Clerk secret key for authentication

## Development Guidelines

This project follows Django best practices as defined in `.cursor/rules/django.mdc`:

### Code Style
- Follow Django's MVT pattern with clear separation of concerns
- Use Django's built-in features and tools wherever possible
- Prioritize readability and maintainability (PEP 8 compliance)
- Use descriptive variable and function names with Django conventions

### Django-Specific Practices
- Use Django Ninja for API development (already implemented)
- Keep business logic in models and forms; keep views light
- Leverage Django's ORM for database interactions
- Use Django's built-in authentication framework with custom User model
- Implement proper error handling at the view level

### Performance Optimization
- Use `select_related` and `prefetch_related` for related object fetching
- Implement caching with Redis backend when needed
- Use asynchronous views for I/O-bound operations
- Optimize static file handling with WhiteNoise (already configured)

### Security
- Apply Django's security best practices (CSRF protection, XSS prevention)
- Use Django's built-in validation framework
- Implement proper error handling and custom error pages