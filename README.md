# Smart Chat AI

A production-ready AI chat API with persistent memory, analytics, and secure auth. Built with FastAPI, PostgreSQL, Redis, and NGINX.

## Overview

- Lightweight API for conversation storage and AI-driven replies
- Dockerized for easy local development and production deployment
- Includes CI/CD with GitHub Actions

## Quick Start (Docker)

1. Copy environment template:

```bash
copy .env.example .env   # Windows
cp .env.example .env     # macOS / Linux
```

2. Start services:

```bash
docker-compose up -d --build
docker-compose ps
```

3. Open API docs:

- Swagger: http://localhost:8000/docs
- Health:  http://localhost:8000/health

## Requirements

- Docker & Docker Compose (recommended)
- Python 3.11+ (for local development)
- Git

## Configuration

Copy `.env.example` to `.env` and set values. Important variables:

```
DEBUG=False
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://chatuser:password@db:5432/chatdb
REDIS_URL=redis://cache:6379/0
OPENAI_API_KEY=sk-...
```

Do not commit `.env` to source control. The repository ignores `.env` and `.env.example`.

## Development (Local without Docker)

1. Create and activate a virtualenv:

```bash
python -m venv venv
venv\Scripts\activate    # Windows
source venv/bin/activate   # macOS / Linux
```

2. Install dependencies and run:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Testing

Run tests inside the app container or locally:

```bash
docker-compose exec app pytest -v
# or
pytest -v
```

## CI/CD

This repository includes a GitHub Actions workflow that builds, tests, and deploys to an EC2 host. To enable deployment, add these repository secrets in GitHub:

- `DEPLOY_KEY` (SSH private key)
- `DEPLOY_HOST` (server hostname)
- `DEPLOY_USER` (server user, e.g. ubuntu)
- `DEPLOY_PATH` (deployment directory on server)

The workflow writes the private key from `DEPLOY_KEY` to `~/.ssh/deploy_key` and uses it to SSH to the host.

## Useful Commands

```bash
docker-compose logs -f app
docker-compose restart app
docker-compose down -v
docker-compose build --no-cache
```

## Contributing

1. Fork repository
2. Create a feature branch
3. Add tests and update docs
4. Open a pull request

## License

MIT

---

For more details, check the project files and the `scripts/` folder for deployment helpers.

Happy building! 🚀