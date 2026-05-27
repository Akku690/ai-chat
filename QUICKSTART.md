# 🚀 Quick Start - Run Project in 5 Minutes

## ⚠️ CRITICAL: Start Docker Desktop First!

**Status**: ❌ Docker daemon is NOT running

### Windows 10/11
1. Open **Start Menu**
2. Search for **"Docker Desktop"**
3. Click to launch
4. Wait 30-60 seconds (watch system tray)
5. When started: Green whale icon ✅

### Verify Docker Started
```powershell
docker ps
# Should show list (not error)
```

---

## Step 1: Navigate to Project

```powershell
cd "C:\Users\Akanksha Singh\Downloads\ai chat"
```

---

## Step 2: Verify Configuration

**Status**: ✅ Already configured

```powershell
# Check .env exists
dir .env

# View configuration
cat .env
```

Current configuration:
- ✅ `SECRET_KEY` generated and set
- ✅ Database credentials configured
- ✅ Redis configured
- ✅ OPENAI_API_KEY placeholder ready

---

## Step 3: Start All Services

### Option A: Quick Setup (with defaults)

```bash
# Copy environment template
copy .env.example .env
```

Default values are safe for development. To use AI features:

```bash
# Edit .env and add your OpenAI API key
notepad .env
```

Update these lines:
```env
SECRET_KEY=your-generated-key-here
OPENAI_API_KEY=sk-your-openai-key-here
```

### Option B: Custom Setup

```bash
# Generate a secure SECRET_KEY
# Windows PowerShell:
[System.Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes((New-Guid).ToString())) | Set-Clipboard

# macOS/Linux:
openssl rand -hex 32 | pbcopy
```

Edit `.env`:
```env
DEBUG=False
SECRET_KEY=<your-generated-key>
DB_USER=chatuser
DB_PASSWORD=<your-password>
OPENAI_API_KEY=<your-openai-key>
```

---

## Step 3: Start Docker Services

### ⚠️ MUST START DOCKER DESKTOP FIRST (see top)

Then run:

```powershell
# Start all services
docker-compose up -d

# Wait 15-30 seconds for services to start
```

Expected output:
```
[+] Running 4/4
  ✓ Container chat-db      Started
  ✓ Container chat-cache   Started
  ✓ Container chat-app     Started
  ✓ Container chat-nginx   Started
```

---

## Step 4: Verify Installation

### Check Service Health

```powershell
# Verify all services running
docker-compose ps

# Should show 4 containers with status "Up"
```

### Check API Health

```powershell
# Via curl
curl http://localhost:8000/health

# Expected response:
# {"status":"healthy","database":true,"redis":true,"ai_service":false}
```

---

## Step 4: Start Docker Services

### Method 1: Using VS Code Tasks (Recommended)

1. Press `Ctrl+Shift+P`
2. Type "Tasks: Run Task"
3. Select "Docker: Up"

### Method 2: Using Terminal

```bash
# Start all services
docker-compose up -d

# Wait for services to be ready (30 seconds)
# Then verify:
docker-compose ps
```

Expected output:
```
NAME          STATUS
chat-app      Up (healthy)
chat-db       Up (healthy)
chat-cache    Up (healthy)
chat-nginx    Up
```

---

## Step 5: Verify Installation

### Check Service Health

```bash
# Via curl
curl http://localhost:8000/health

# Expected response:
# {"status":"healthy","database":true,"redis":true,"ai_service":false}
```

### Check Logs

```bash
# View all logs
docker-compose logs -f

# Or use VS Code Task: Docker: Logs

# View specific service
docker-compose logs -f app
```

---

## Step 6: Access the Application

### 🌐 Web Interface

Open these in your browser:

| URL | Purpose |
|-----|---------|
| http://localhost:8000 | API welcome page |
| http://localhost:8000/docs | **Swagger UI (Interactive)** ⭐ |
| http://localhost:8000/redoc | ReDoc (Alternative docs) |
| http://localhost:8000/health | Health check endpoint |

### 📚 API Documentation

The Swagger UI at http://localhost:8000/docs is interactive:

1. Click any endpoint to expand it
2. Click "Try it out" button
3. Fill in parameters
4. Click "Execute"
5. See response immediately

---

## Step 7: Test the API

### Using Swagger UI (Easiest)

1. Go to http://localhost:8000/docs
2. Expand `POST /auth/register`
3. Click "Try it out"
4. Enter:
   ```json
   {
     "email": "test@example.com",
     "username": "testuser",
     "password": "password123"
   }
   ```
5. Click "Execute"
6. See the response!

### Using curl (Terminal)

```bash
# 1. Register
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "password123"
  }'

# 2. Login (copy the token)
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'

# 3. Create conversation (use the token)
TOKEN="<paste-token-from-step-2>"
curl -X POST http://localhost:8000/conversations \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "My First Chat"}'

# 4. Send a message
CONV_ID=1  # from step 3 response
curl -X POST http://localhost:8000/conversations/$CONV_ID/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, how are you?"}'
```

---

## Step 8: Useful Commands

### Docker Management

```bash
# View all services
docker-compose ps

# View logs
docker-compose logs -f

# Stop services (keep data)
docker-compose stop

# Start stopped services
docker-compose start

# Restart services
docker-compose restart

# Stop and remove containers (keep volumes)
docker-compose down

# Stop and remove everything (DELETE ALL DATA)
docker-compose down -v

# Rebuild images
docker-compose build

# Rebuild without cache
docker-compose build --no-cache
```

### Database Access

```bash
# Access PostgreSQL shell
docker-compose exec db psql -U chatuser -d chatdb

# Useful commands in psql:
# \dt                    - List tables
# \d users               - Describe table
# SELECT * FROM users;   - Query table
# \q                     - Quit
```

### Application Debugging

```bash
# View app logs
docker-compose logs -f app

# Run commands in app container
docker-compose exec app python -c "import app; print('OK')"

# Connect to app shell
docker-compose exec app bash

# Run tests
docker-compose exec app pytest
```

---

## Step 9: VS Code Extensions

Recommended extensions (auto-suggested in workspace):

- **Python** - Language support
- **Pylance** - IntelliSense & type checking
- **Docker** - Docker management
- **Thunder Client** - API testing (like Postman)
- **GitLens** - Git integration

Install:
1. Open Extensions (`Ctrl+Shift+X`)
2. Search for each extension
3. Click "Install"

Or use workspace recommendations:
1. VS Code shows "Show Extensions" notification
2. Click and install recommended extensions

---

## Step 10: Common Issues & Solutions

### ❌ Services won't start

```bash
# 1. Check Docker is running
docker ps

# 2. View error logs
docker-compose logs

# 3. Rebuild everything
docker-compose down -v
docker-compose build
docker-compose up -d
```

### ❌ Port already in use

```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill process (Windows)
taskkill /PID <PID> /F

# Or change port in docker-compose.yml
```

### ❌ Database connection error

```bash
# Check database service
docker-compose logs db

# Restart database
docker-compose restart db

# Wait 10 seconds then check health
curl http://localhost:8000/health
```

### ❌ API returns 500 error

```bash
# Check app logs
docker-compose logs app

# May need to rebuild
docker-compose rebuild app
docker-compose up -d app
```

### ❌ Can't access http://localhost:8000

```bash
# 1. Check if services are running
docker-compose ps

# 2. Wait 30 seconds for startup
# 3. Check health endpoint
curl http://localhost:8000/health

# 4. If still fails, check logs
docker-compose logs app
```

---

## Next Steps

### 📚 Learn More

Read these documentation files:
1. **README.md** - Project overview
2. **DEVELOPMENT.md** - Local development guide
3. **SECURITY.md** - Before production

### 🔧 Development Tasks

1. **Explore the code** - Start with `app/main.py`
2. **Create test users** - Via Swagger UI
3. **Test conversations** - Create and chat
4. **Review database** - Use PostgreSQL shell
5. **Check Redis cache** - Via `redis-cli`

### 🚀 Advanced Setup

1. **Add OPENAI_API_KEY** - For real AI responses
2. **Configure CORS** - For frontend integration
3. **Set up testing** - Run pytest
4. **Review security** - Read SECURITY.md

---

## 📞 Quick Reference

| Task | Command |
|------|---------|
| Start all | `docker-compose up -d` |
| Stop all | `docker-compose stop` |
| View logs | `docker-compose logs -f` |
| Health check | `curl http://localhost:8000/health` |
| API docs | http://localhost:8000/docs |
| Restart app | `docker-compose restart app` |
| Full cleanup | `docker-compose down -v` |

---

## ✅ Verification Checklist

- [ ] Python 3.11+ installed
- [ ] Docker running
- [ ] `.env` file created
- [ ] Services started (`docker-compose up -d`)
- [ ] Health check passes (`curl http://localhost:8000/health`)
- [ ] Swagger UI loads (http://localhost:8000/docs)
- [ ] Can register user via API
- [ ] Can create conversation
- [ ] Can send message

---

## 🎯 You're Ready!

If all checks pass, your Smart Chat AI is running! 🚀

- **API Available at:** http://localhost:8000
- **Documentation at:** http://localhost:8000/docs
- **Health Status:** http://localhost:8000/health

### Next: Read DEVELOPMENT.md for deeper learning!

---

**Questions?** Check the relevant documentation file or review logs with `docker-compose logs -f`
