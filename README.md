# Smart Chat API with Memory

A production-ready AI-powered chat application with persistent memory, real-time analytics, and secure authentication. Built with FastAPI, PostgreSQL, Redis, and NGINX.

## 🚀 Features

- **AI Integration**: OpenAI ChatGPT integration for intelligent responses
- **Persistent Memory**: Full conversation history with PostgreSQL
- **Caching Layer**: Redis for high-performance response caching
- **User Authentication**: Secure JWT-based authentication
- **Analytics**: Real-time usage tracking and statistics
- **Docker Ready**: Complete containerization with Docker Compose
- **CI/CD Pipeline**: GitHub Actions for automated testing and deployment
- **Security**: SSL/TLS, rate limiting, security headers, non-root containers
- **API Documentation**: Auto-generated Swagger UI at `/docs`

## 📋 Prerequisites

- Docker & Docker Compose
- Python 3.11+ (for local development)
- OpenAI API key (optional, for live AI features)
- Git

## 🔧 Quick Start

### 1. Clone or Download Project

```bash
cd "C:\Users\Akanksha Singh\Downloads\ai chat"
```

### 2. Setup Environment

```bash
# Copy environment template
copy .env.example .env

# Edit .env with your configuration
# At minimum, set SECRET_KEY and OPENAI_API_KEY
```

### 3. Start Services

```bash
# Build and start all services
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f app
```

### 4. Access Application

- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **HTTPS**: https://localhost (self-signed certificate)
- **Health Check**: http://localhost:8000/health

## 📚 API Endpoints

### Authentication
```
POST   /auth/register       - Register new user
POST   /auth/login          - Login and get token
GET    /auth/me             - Get current user info
```

### Conversations
```
POST   /conversations       - Create new conversation
GET    /conversations       - List user conversations
GET    /conversations/{id}  - Get conversation details
PUT    /conversations/{id}  - Update conversation title
DELETE /conversations/{id}  - Delete conversation
```

### Messages & Chat
```
GET    /conversations/{id}/messages     - Get conversation messages
POST   /conversations/{id}/chat         - Send message and get AI response
```

### Analytics
```
GET    /analytics/stats    - Get user statistics and usage
```

### Health
```
GET    /health             - Service health check
```

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│       NGINX (Port 443)              │
│   - SSL/TLS Termination             │
│   - Rate Limiting                   │
│   - Request Routing                 │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│    FastAPI Application (8000)       │
│  - User Authentication              │
│  - Conversation Management          │
│  - AI Integration                   │
└──────────────┬──────────────────────┘
               │
      ┌────────┼────────┐
      │        │        │
┌─────▼───┐ ┌──▼──┐ ┌───▼─────┐
│PostgreSQL│ │Redis│ │OpenAI   │
│  (5432)  │ │(6379)│ │API      │
└──────────┘ └──────┘ └─────────┘
```

## 🐳 Docker Compose Services

| Service | Image | Port | Purpose |
|---------|-------|------|---------|
| app | Python 3.11 | 8000 | FastAPI application |
| db | PostgreSQL 15 | 5432 | Data persistence |
| cache | Redis 7 | 6379 | Response caching |
| nginx | NGINX Alpine | 80, 443 | Reverse proxy & SSL |

## 🔐 Security Features

- ✅ Non-root container users
- ✅ SSL/TLS encryption (HTTPS)
- ✅ JWT token authentication
- ✅ Rate limiting (10 req/s general, 5 req/m for auth)
- ✅ Security headers (X-Frame-Options, CSP, etc.)
- ✅ Password hashing with bcrypt
- ✅ SQL injection protection (SQLAlchemy ORM)
- ✅ CORS configuration
- ✅ Resource limits per container

## 📝 Environment Variables

See `.env.example` for all available options:

```env
DEBUG=False                                    # Debug mode
SECRET_KEY=your-secret-key                     # JWT secret
DB_USER=chatuser                               # PostgreSQL user
DB_PASSWORD=chatpass                           # PostgreSQL password
DB_NAME=chatdb                                 # Database name
REDIS_PASSWORD=redispass                       # Redis password
OPENAI_API_KEY=sk-...                         # OpenAI API key
OPENAI_MODEL=gpt-3.5-turbo                    # Model name
```

## 🧪 Testing

```bash
# Run tests
docker-compose exec app pytest

# Run with coverage
docker-compose exec app pytest --cov=app

# Run specific test file
docker-compose exec app pytest tests/test_auth.py
```

## 📊 Database Migrations

The database initializes automatically on first run. For custom migrations:

```bash
# Access database shell
docker-compose exec db psql -U chatuser -d chatdb

# Backup database
docker-compose exec db pg_dump -U chatuser chatdb > backup.sql
```

## 🔄 Useful Commands

```bash
# View all logs
docker-compose logs -f

# View app logs only
docker-compose logs -f app

# Restart specific service
docker-compose restart app

# Stop all services
docker-compose stop

# Remove all containers and volumes
docker-compose down -v

# Rebuild images
docker-compose build --no-cache

# Run command in app container
docker-compose exec app python -c "import app"
```

## 🚀 Deployment

### Option 1: Manual Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

### Option 2: GitHub Actions CI/CD

The project includes automated CI/CD pipeline. To enable:

1. Push code to GitHub repository
2. Configure GitHub secrets:
   - `DEPLOY_KEY`: SSH private key
   - `DEPLOY_HOST`: Server hostname
   - `DEPLOY_USER`: SSH username
   - `DEPLOY_PATH`: Deployment directory

3. Pipeline automatically:
   - Builds Docker image
   - Runs tests
   - Pushes to container registry
   - Deploys to server

## 🔒 SSL/TLS Setup

### Development (Self-signed)
Already configured with self-signed certificates.

### Production (Let's Encrypt)
```bash
# Run Certbot in container
docker run -it --rm -v $PWD/nginx/ssl:/etc/letsencrypt \
  certbot/certbot certonly --standalone -d yourdomain.com
```

See [SECURITY.md](SECURITY.md) for detailed SSL configuration.

## 📖 Additional Documentation

- [DEVELOPMENT.md](DEVELOPMENT.md) - Local development guide
- [DEPLOYMENT.md](DEPLOYMENT.md) - Production deployment guide
- [SECURITY.md](SECURITY.md) - Security configuration guide
- [API.md](API.md) - Detailed API documentation

## 🐛 Troubleshooting

### Services won't start
```bash
# Check logs
docker-compose logs app

# Verify .env file exists
ls -la .env

# Check port availability
netstat -tuln | grep 8000
```

### Database connection error
```bash
# Check database status
docker-compose logs db

# Reset database
docker-compose down -v
docker-compose up -d db
```

### Redis connection error
```bash
# Test Redis connection
docker-compose exec cache redis-cli ping

# Check Redis logs
docker-compose logs cache
```

## 📞 Support

For issues and questions:
1. Check existing documentation
2. Review Docker logs: `docker-compose logs -f`
3. Check service health: `curl http://localhost:8000/health`

## 📄 License

MIT License - See LICENSE file for details

## 🎯 Next Steps

1. ✅ Update `.env` with your OpenAI API key
2. ✅ Test API endpoints at http://localhost:8000/docs
3. ✅ Customize NGINX configuration as needed
4. ✅ Review SECURITY.md for production setup
5. ✅ Configure GitHub secrets for CI/CD deployment

---

**Happy building! 🚀**
#   a i - c h a t  
 