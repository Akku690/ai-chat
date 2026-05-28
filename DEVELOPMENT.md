# Development Guide

## 🛠️ Local Development Setup

Complete guide for setting up the Smart Chat API for local development.

## Prerequisites

- Python 3.11+
- Docker & Docker Compose
- Git
- Your favorite code editor (VS Code recommended)
- Postman or curl (for API testing)

## 🚀 Quick Start

### 1. Clone Repository

```bash
cd "C:\Users\Akanksha Singh\Downloads\ai chat"
```

### 2. Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Setup Environment

```bash
# Copy template
cp .env.example .env

# Edit .env file
# Set DEBUG=True for development
# Add your OPENAI_API_KEY if testing AI features
```

### 4. Start Services

```bash
# Using Docker Compose (recommended)
docker-compose up -d

# Check services
docker-compose ps

# View logs
docker-compose logs -f
```

### 5. Access Application

- **API**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

## 📝 Project Structure

```
smart-chat-ai/
├── app/
│   ├── __init__.py
│   ├── config.py           # Settings
│   ├── database.py         # Database connection
│   ├── main.py             # FastAPI app
│   ├── schemas.py          # Pydantic models
│   ├── security.py         # JWT & auth
│   ├── models/              SQLAlchemy models
│   │   ├── user.py
│   │   ├── conversation.py
│   │   ├── message.py
│   │   └── analytics.py
│   ├── routes/             # API endpoints
│   │   ├── auth.py
│   │   ├── conversations.py
│   │   ├── analytics.py
│   │   └── health.py
│   └── services/           # Business logic
│       ├── cache.py        # Redis
│       ├── ai.py           # AI integration
│       └── database.py     # DB operations
├── nginx/
│   └── nginx.conf          # NGINX config
├── scripts/
│   ├── setup.sh            # Setup script
│   ├── cleanup.sh          # Cleanup script
│   └── deploy.sh           # Deploy script
├── .github/workflows/      # CI/CD
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

## 🧪 Testing

### Run All Tests

```bash
# With Docker
docker-compose exec app pytest

# Locally
pytest
```

### Run Specific Tests

```bash
# Test auth module
pytest tests/test_auth.py

# Test with verbose output
pytest -v

# Test with coverage
pytest --cov=app --cov-report=html
```

### Create Test File

```python
# tests/test_example.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
```

## 🔧 Common Development Tasks

### Add New Endpoint

1. Create schema in `app/schemas.py`:
```python
class NewFeatureResponse(BaseModel):
    id: int
    data: str
```

2. Create route in `app/routes/new_feature.py`:
```python
from fastapi import APIRouter

router = APIRouter(prefix="/new-feature", tags=["new_feature"])

@router.get("/{id}", response_model=NewFeatureResponse)
async def get_feature(id: int):
    return {"id": id, "data": "example"}
```

3. Register route in `app/main.py`:
```python
from app.routes.new_feature import router as new_feature_router
app.include_router(new_feature_router)
```

### Add Database Model

1. Create model in `app/models/new_model.py`:
```python
from sqlalchemy import Column, String, Integer
from app.database import Base

class NewModel(Base):
    __tablename__ = "new_models"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
```

2. Update `app/models/__init__.py`:
```python
from app.models.new_model import NewModel
```

3. Run migration (database auto-creates on startup)

### Update Environment Variables

1. Edit `.env` file
2. Add to `app/config.py`:
```python
NEW_SETTING: str = os.getenv("NEW_SETTING", "default_value")
```

3. Access in code:
```python
from app.config import settings
print(settings.NEW_SETTING)
```

## 📊 Database Operations

### Access Database Shell

```bash
# PostgreSQL
docker-compose exec db psql -U chatuser -d chatdb

# Useful commands:
\dt                 # List tables
\d table_name       # Describe table
SELECT * FROM users; # Query
\q                  # Quit
```

### Create Backup

```bash
docker-compose exec db pg_dump -U chatuser chatdb > backup.sql
```

### Restore from Backup

```bash
docker-compose exec -T db psql -U chatuser chatdb < backup.sql
```

### Reset Database

```bash
# WARNING: Deletes all data
docker-compose down -v
docker-compose up -d db
```

## 🔍 Debugging

### Enable Debug Mode

```env
# .env
DEBUG=True
```

### Print Logs

```python
import logging

logger = logging.getLogger(__name__)
logger.info("Debug message")
logger.error("Error message")
```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f app

# Last 100 lines
docker-compose logs --tail=100 app
```

### Use Python Debugger

```python
# In your code
import pdb; pdb.set_trace()

# Then interact in the debugger
(Pdb) p variable_name  # Print variable
(Pdb) c                # Continue execution
```

### Inspect Container

```bash
# Connect to app container
docker-compose exec app bash

# Run Python commands
python
>>> from app.config import settings
>>> print(settings.DATABASE_URL)
```

## 🎯 API Testing

### Using Swagger UI

1. Go to: http://localhost:8000/docs
2. Click "Try it out" on any endpoint
3. Fill in parameters and click "Execute"

### Using curl

```bash
# Health check
curl http://localhost:8000/health

# Register user
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "testuser",
    "password": "password123"
  }'

# Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'

# Save token for subsequent requests
TOKEN="eyJ0eXAiOiJKV1QiLCJhbGc..."

# Create conversation (authenticated)
curl -X POST http://localhost:8000/conversations \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "My Chat"}'
```

### Using Postman

1. Download [Postman](https://www.postman.com)
2. Import request from Swagger: http://localhost:8000/openapi.json
3. Create requests and organize in collections
4. Use environment variables for base URL and tokens

Example environment:
```json
{
  "base_url": "http://localhost:8000",
  "token": ""
}
```

## 🔄 Hot Reload

FastAPI supports hot reload during development:

```bash
# Running locally with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or using Docker
docker-compose.yml already mounts app volume for reload
```

The server automatically restarts when you modify files.

## 📦 Managing Dependencies

### Add New Package

```bash
# Install
pip install package-name

# Update requirements.txt
pip freeze > requirements.txt

# Or add manually to requirements.txt
echo "package-name==1.0.0" >> requirements.txt

# Rebuild Docker image
docker-compose build
```

### Remove Package

```bash
pip uninstall package-name
pip freeze > requirements.txt
docker-compose build
```

### Check Installed Packages

```bash
pip list
pip show package-name
```

## 🎨 Code Style

### Format Code

```bash
# Using black
pip install black
black app/

# Using autopep8
pip install autopep8
autopep8 --in-place --aggressive --aggressive app/**/*.py
```

### Lint Code

```bash
# Using pylint
pip install pylint
pylint app/

# Using flake8
pip install flake8
flake8 app/
```

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org)
- [Redis Documentation](https://redis.io/docs)
- [PostgreSQL Documentation](https://www.postgresql.org/docs)
- [Docker Documentation](https://docs.docker.com)

## 🚨 Common Issues

### Port Already in Use

```bash
# Find and kill process
lsof -i :8000
kill -9 <PID>
```

### Import Errors

```bash
# Reinstall dependencies
pip install -r requirements.txt

# Clear Python cache
find . -type d -name __pycache__ -exec rm -rf {} +
```

### Database Connection Failed

```bash
# Check database status
docker-compose ps

# View database logs
docker-compose logs db

# Restart database
docker-compose restart db
```

### Redis Connection Failed

```bash
# Check Redis status
docker-compose ps cache

# Test Redis connection
redis-cli ping

# Restart Redis
docker-compose restart cache
```

## 💡 Tips & Tricks

### Access Environment Variables Programmatically

```python
from app.config import settings

print(settings.DATABASE_URL)
print(settings.OPENAI_API_KEY)
print(settings.DEBUG)
```

### Test AI Endpoint Without API Key

```python
# AI service returns mock response when API key is not configured
# This allows development without OpenAI subscription
```

### Monitor Resource Usage

```bash
# Docker stats
docker stats

# Check logs size
du -sh logs/
```

### Reload Services Without Restart

```bash
# Reload nginx config
docker-compose exec nginx nginx -s reload

# Restart specific service
docker-compose restart app
```

---

Happy developing! 🚀
