# Smart Chat API - Complete Requirements

## 🔧 System Requirements

### Minimum Hardware
- **CPU**: 2 cores
- **RAM**: 4 GB (8 GB recommended)
- **Disk Space**: 10 GB
- **OS**: Windows 10+, macOS, or Linux

### Recommended Hardware
- **CPU**: 4 cores
- **RAM**: 8 GB
- **Disk Space**: 20 GB

---

## 📦 Software Requirements

### Required Software

#### 1. **Docker Desktop** ⚠️ CRITICAL
- **Purpose**: Container runtime and orchestration
- **Version**: Docker 20.10+
- **Download**: https://www.docker.com/products/docker-desktop
- **Verification**:
  ```powershell
  docker --version
  docker-compose --version
  ```
- **Status**: ❌ NOT RUNNING (needs to be started)

#### 2. **Python** (Optional for local development)
- **Purpose**: Run application outside Docker
- **Version**: Python 3.11+
- **Download**: https://www.python.org/downloads/
- **Verification**:
  ```powershell
  python --version
  ```

#### 3. **Git** (Recommended)
- **Purpose**: Version control
- **Version**: Any recent version
- **Download**: https://git-scm.com/
- **Verification**:
  ```powershell
  git --version
  ```

---

## 🐳 Docker Services Requirements

### 4 Container Services

| # | Service | Image | Resource Limits | Purpose |
|---|---------|-------|-----------------|---------|
| 1 | **FastAPI App** | `python:3.11-slim` | 512MB RAM, 0.5 CPU | Backend API |
| 2 | **PostgreSQL** | `postgres:15-alpine` | 1GB RAM, 1 CPU | Database |
| 3 | **Redis** | `redis:7-alpine` | 256MB RAM, 0.5 CPU | Cache Layer |
| 4 | **NGINX** | `nginx:alpine` | 256MB RAM, 0.25 CPU | Reverse Proxy |

**Total Resources**: ~2GB RAM, 2 CPU cores

---

## 📚 Python Dependencies (requirements.txt)

### Backend Framework
```
fastapi==0.104.1              # Web framework
uvicorn[standard]==0.24.0     # ASGI server
python-multipart==0.0.6       # Form data handling
```

### Database & ORM
```
sqlalchemy==2.0.23            # ORM
psycopg2-binary==2.9.9        # PostgreSQL adapter
```

### Caching & Session
```
redis==5.0.1                  # Redis client
```

### Authentication & Security
```
python-jose[cryptography]==3.3.0   # JWT tokens
passlib[bcrypt]==1.7.4             # Password hashing
```

### Data Validation
```
pydantic-settings==2.1.0      # Settings management
pydantic[email]==2.5.0        # Data validation
```

### HTTP & Requests
```
httpx==0.25.1                 # Async HTTP client
requests==2.31.0              # HTTP requests
```

### AI Integration
```
openai==1.3.9                 # OpenAI API client (optional)
```

---

## 🌐 Network Requirements

### Ports Used

| Port | Service | Protocol | Access |
|------|---------|----------|--------|
| **80** | NGINX HTTP | HTTP | Local |
| **443** | NGINX HTTPS | HTTPS | Local |
| **8000** | FastAPI | HTTP | Local |
| **5432** | PostgreSQL | TCP | Internal only |
| **6379** | Redis | TCP | Internal only |

### Firewall Rules (for production)
- Allow HTTP (80) from public
- Allow HTTPS (443) from public
- Allow PostgreSQL (5432) from app container only
- Allow Redis (6379) from app container only

---

## 💾 Storage Requirements

### Volumes/Data
```
postgres_data/        # Database persistence (~500MB initial)
redis_data/           # Cache persistence (~100MB initial)
nginx/ssl/            # SSL certificates
```

### Free Disk Space Needed
- **Minimum**: 5GB
- **Recommended**: 10GB

---

## 🔐 Security Requirements

### Secrets & Credentials
- ✅ **SECRET_KEY**: Generated (FGPl3djEmtZVIstatX_6AetI-M6nr3ayMEC9Z1jKpzE)
- ✅ **DB_PASSWORD**: chatpass (change in production)
- ✅ **REDIS_PASSWORD**: redispass (change in production)
- ⚠️ **OPENAI_API_KEY**: Optional (for AI features)

### SSL/TLS
- **Development**: Self-signed certificates (auto-generated)
- **Production**: Let's Encrypt certificates required

### Access Control
- Non-root container users
- JWT authentication for API
- Rate limiting enabled

---

## 📋 Configuration Files

| File | Purpose | Status |
|------|---------|--------|
| `.env` | Environment variables | ✅ Created |
| `docker-compose.yml` | Service orchestration | ✅ Ready |
| `Dockerfile` | App container image | ✅ Ready |
| `nginx/nginx.conf` | Reverse proxy config | ✅ Ready |
| `requirements.txt` | Python dependencies | ✅ Ready |

---

## ✅ Pre-Launch Checklist

### Step 1: Verify Software
- [ ] Docker Desktop installed: `docker --version`
- [ ] Docker Compose available: `docker-compose --version`
- [ ] Docker daemon is running (see instructions below)

### Step 2: Verify Configuration
- [ ] `.env` file exists: ✅
- [ ] `.env` has valid SECRET_KEY: ✅
- [ ] `docker-compose.yml` exists: ✅
- [ ] `requirements.txt` exists: ✅

### Step 3: Verify Resources
- [ ] At least 2GB free RAM
- [ ] At least 5GB free disk space
- [ ] Ports 80, 443, 8000 are available

### Step 4: Start Services
- [ ] Start Docker Desktop
- [ ] Run: `docker-compose up -d`
- [ ] Verify: `docker-compose ps`

---

## 🚀 Starting Docker Desktop

### Windows 10/11
1. Open **Start Menu**
2. Search for **"Docker Desktop"**
3. Click to launch
4. Wait for Docker to start (icon in system tray)
5. Verify: Run `docker ps` in PowerShell

### Alternative (Command Line)
```powershell
# Start Docker Desktop service
& 'C:\Program Files\Docker\Docker\Docker Desktop.exe'

# Or start Docker engine directly
wsl --list --verbose  # Check if WSL 2 is installed
```

### macOS
```bash
# Start Docker Desktop
open /Applications/Docker.app

# Or via terminal
docker ps
```

### Linux
```bash
# Start Docker daemon
sudo systemctl start docker
sudo systemctl enable docker

# Verify
docker ps
```

---

## 🔍 Current Setup Status

| Component | Status | Details |
|-----------|--------|---------|
| Project Location | ✅ Ready | C:\Users\Akanksha Singh\Downloads\ai chat |
| .env File | ✅ Created | With SECRET_KEY configured |
| Docker Compose | ✅ Installed | v5.1.3 |
| Docker Desktop | ❌ NOT RUNNING | Must be started |
| Python | ✅ Available | Version available |
| All Services | ⏳ Pending | Will start after Docker runs |

---

## 📝 Environment Variables

Current `.env` Configuration:
```env
DEBUG=False
SECRET_KEY=FGPl3djEmtZVIstatX_6AetI-M6nr3ayMEC9Z1jKpzE
DB_USER=chatuser
DB_PASSWORD=chatpass
DB_NAME=chatdb
REDIS_PASSWORD=redispass
OPENAI_API_KEY=sk-test-key-optional-for-development
OPENAI_MODEL=gpt-3.5-turbo
```

### For Production (Change These)
```env
DEBUG=False                    # CRITICAL: Keep False
SECRET_KEY=<generate-new>     # Generate new random key
DB_PASSWORD=<strong-password> # Change to strong password
REDIS_PASSWORD=<strong-password> # Change to strong password
OPENAI_API_KEY=sk-...         # Add your OpenAI key
```

---

## 🎯 Next Steps

### Immediate (5 minutes)
1. **Start Docker Desktop** (see instructions above)
2. Verify Docker running: `docker ps`
3. Start services: `docker-compose up -d`
4. Check status: `docker-compose ps`

### Then (10 minutes)
5. Visit API: http://localhost:8000/docs
6. Test endpoints in Swagger UI
7. Create test user and conversation

### Later (30-60 minutes)
8. Read `DEVELOPMENT.md` for local development
9. Review `DEPLOYMENT.md` for production
10. Read `SECURITY.md` for hardening

---

## 🐛 Troubleshooting

### Docker Not Running?
```powershell
# Check status
docker ps

# If error appears, start Docker Desktop manually
# See "Starting Docker Desktop" section above
```

### Port Already in Use?
```powershell
# Find process on port 8000
netstat -ano | findstr :8000

# Kill process
taskkill /PID <PID> /F
```

### Services Won't Start?
```powershell
# Check logs
docker-compose logs -f

# Reset everything
docker-compose down -v
docker-compose build
docker-compose up -d
```

---

## 📊 Resource Monitoring

### View Running Containers
```powershell
docker-compose ps
```

### View Resource Usage
```powershell
docker stats
```

### View Logs
```powershell
docker-compose logs -f app
docker-compose logs -f db
docker-compose logs -f cache
docker-compose logs -f nginx
```

---

## ✨ When Everything is Running

### API Endpoints
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health
- **HTTPS**: https://localhost (self-signed)

### Services
- **Database**: localhost:5432 (psql)
- **Cache**: localhost:6379 (redis-cli)
- **App**: localhost:8000 (FastAPI)

### Default Credentials (Development)
```
Database User: chatuser
Database Password: chatpass
Redis Password: redispass
```

---

## 📞 Support

| Issue | Solution |
|-------|----------|
| Docker won't start | See "Starting Docker Desktop" |
| Port conflict | Kill existing process using port |
| Containers fail | Check logs: `docker-compose logs` |
| Database connection error | Verify .env file and restart |
| API not responding | Check: `docker-compose ps` |

---

## 📚 Further Reading

- [README.md](README.md) - Project overview
- [DEVELOPMENT.md](DEVELOPMENT.md) - Development guide
- [DEPLOYMENT.md](DEPLOYMENT.md) - Production setup
- [SECURITY.md](SECURITY.md) - Security hardening

---

**Status**: ⏳ **Ready to Launch** - Start Docker Desktop to begin!
