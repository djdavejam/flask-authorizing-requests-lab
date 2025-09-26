# Flask Authorization Lab - Complete Solution

A Flask API that implements session-based authentication and authorization for a blog application.

## Features

- User login/logout with session management
- Public articles accessible to all users
- Member-only articles restricted to authenticated users
- Authorization middleware that returns 401 for unauthorized access

## Setup

1. **Install dependencies:**
   ```bash
   pipenv install && pipenv shell
   cd server
   ```

2. **Initialize database:**
   ```bash
   flask shell
   ```
   ```python
   from config import app, db
   from models import User, Article
   db.drop_all()
   db.create_all()
   exit()
   ```

3. **Seed database:**
   ```bash
   python seed.py
   ```

4. **Run application:**
   ```bash
   python app.py
   ```

## API Endpoints

### Public Endpoints
- `GET /articles` - Get all articles
- `GET /articles/<id>` - Get specific article (with page view limit)
- `POST /login` - Login user
- `DELETE /logout` - Logout user
- `GET /check_session` - Check if user is logged in

### Protected Endpoints (Require Authentication)
- `GET /members_only_articles` - Get all member-only articles
- `GET /members_only_articles/<id>` - Get specific member-only article

## Authorization Implementation

The authorization is implemented using Flask sessions:

```python
def get(self):
    # Check if user is logged in
    if not session.get('user_id'):
        return {'message': 'Unauthorized'}, 401
    
    # Return protected content
    return protected_data, 200
```

## Testing

Run the test suite:
```bash
pytest
```

All tests should pass, verifying:
- Unauthorized users get 401 responses
- Authorized users can access member-only content
- Session management works correctly

## Key Files

- `app.py` - Main Flask application with route handlers
- `config.py` - Flask app configuration and database setup
- `models.py` - SQLAlchemy models for User and Article
- `seed.py` - Database seeding script