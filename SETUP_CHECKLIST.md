# ✅ Smart Chat AI - Setup Checklist

## Pre-Startup Checklist

- [ ] **Python 3.11+** installed
  ```powershell
  python --version
  ```

- [ ] **Docker** installed and running
  ```powershell
  docker --version
  docker ps
  ```

- [ ] **Docker Compose** installed
  ```powershell
  docker-compose --version
  ```

- [ ] **Project files** present
  ```powershell
  ls app/main.py
  ls docker-compose.yml
  ```

- [ ] **In correct directory**
  ```powershell
  # Should be: C:\Users\Akanksha Singh\Downloads\ai chat
  pwd
  ```

---

## Environment Setup (Choose One)

### ✅ Option 1: Quick Setup (Recommended for First Time)

```powershell
# Copy environment template
copy .env.example .env

# The defaults are safe for development!
# To use AI features, edit .env and add your OpenAI key
```

### ✅ Option 2: Generate New SECRET_KEY

```powershell
# Generate a secure key and copy to clipboard
[System.Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes((New-Guid).ToString())) | Set-Clipboard

# Paste it into .env file:
# SECRET_KEY=<paste-here>
```

---

## Startup Steps (Do These in Order)

### 1️⃣ Validate Environment Setup

```powershell
# Run the validation script
python scripts/validate_setup.py

# Should show: "✅ All checks passed!"
```

### 2️⃣ Start Docker Services

Choose your method:

**Method A: PowerShell (Recommended)**
```powershell
docker-compose up -d
```

**Method B: VS Code Tasks**
1. Press `Ctrl+Shift+P`
2. Type: "Tasks: Run Task"
3. Select: "Docker: Up"

**Method C: Docker Desktop**
1. Open Docker Desktop
2. Go to "Compose" tab
3. Click "Start"

### 3️⃣ Wait for Services (30-60 seconds)

```powershell
# Check service status
docker-compose ps

# Expected: All services showing "Up" or "healthy"
```

Typical startup time:
- PostgreSQL: 10-15 seconds
- Redis: 5-10 seconds
- FastAPI: 5-10 seconds
- NGINX: 2-5 seconds

### 4️⃣ Verify Services are Healthy

```powershell
# Test health endpoint
curl http://localhost:8000/health

# Expected response:
# {"status":"healthy","database":true,"redis":true,"ai_service":false}
```

### 5️⃣ Access the Application

Open in browser:

| URL | Purpose |
|-----|---------|
| http://localhost:8000 | Welcome page |
| **http://localhost:8000/docs** | **Swagger UI (Use This!)** ⭐ |
| http://localhost:8000/health | Health check |

---

## Post-Startup Verification

### ✅ API is Responding

```powershell
curl http://localhost:8000/health
```

Should return (all true):
```json
{
  "status": "healthy",
  "database": true,
  "redis": true,
  "ai_service": false
}
```

### ✅ Database is Connected

```powershell
# Check database logs
docker-compose logs db

# Should show: "LOG:  database system is ready to accept connections"
```

### ✅ API Documentation Works

1. Open: http://localhost:8000/docs
2. Page should load with interactive API docs
3. Try expanding an endpoint

### ✅ Create a Test User

Using Swagger UI (easiest):
1. Go to http://localhost:8000/docs
2. Find `POST /auth/register`
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
6. Should see 200 response with user data

---

## Troubleshooting During Startup

### ❌ "docker-compose: The term 'docker-compose' is not recognized"

**Solution:**
```powershell
# Install Docker Compose
# Or use: docker compose (newer syntax)
docker compose up -d
```

### ❌ "Cannot connect to Docker daemon"

**Solution:**
1. Open Docker Desktop
2. Wait for it to start (watch the icon)
3. Try again

### ❌ "Port 8000 already in use"

**Solution:**
```powershell
# Find process on port 8000
Get-NetTCPConnection -LocalPort 8000

# Kill process (replace PID)
Stop-Process -Id <PID> -Force

# Or use different port in docker-compose.yml
```

### ❌ "Database connection refused"

**Solution:**
```powershell
# Check database is running
docker-compose logs db

# Restart database
docker-compose restart db

# Wait 15 seconds, then try health check again
```

### ❌ "curl: command not found" (on Windows)

**Solution:** Use PowerShell instead:
```powershell
# This works in PowerShell
(Invoke-WebRequest http://localhost:8000/health).Content

# Or install curl via Windows Store
```

---

## Quick Start: First API Call

### Using Swagger UI (Easiest)

1. Open: http://localhost:8000/docs
2. Click "POST /auth/register" to expand
3. Click "Try it out" button
4. Fill in the form:
   - email: `test@example.com`
   - username: `testuser`
   - password: `password123`
5. Click blue "Execute" button
6. See response below!

### Using PowerShell

```powershell
# 1. Register user
$registerBody = @{
    email = "test@example.com"
    username = "testuser"
    password = "password123"
} | ConvertTo-Json

curl -X POST http://localhost:8000/auth/register `
  -Headers @{"Content-Type"="application/json"} `
  -Body $registerBody

# 2. Login (copy the token from response)
$loginBody = @{
    email = "test@example.com"
    password = "password123"
} | ConvertTo-Json

$loginResponse = curl -X POST http://localhost:8000/auth/login `
  -Headers @{"Content-Type"="application/json"} `
  -Body $loginBody | ConvertFrom-Json

# 3. Create conversation (use token)
$token = $loginResponse.access_token
curl -X POST http://localhost:8000/conversations `
  -Headers @{
    "Authorization"="Bearer $token"
    "Content-Type"="application/json"
  } `
  -Body '{"title":"My First Chat"}'
```

---

## VS Code Workspace Setup

### Open the Workspace

```powershell
# In PowerShell from project directory
code smart-chat-ai.code-workspace
```

Or manually:
1. VS Code → File → Open Workspace from File
2. Select: `smart-chat-ai.code-workspace`

### Install Recommended Extensions

1. You'll see notification: "This workspace has extension recommendations"
2. Click "Install Extensions" button
3. Wait for extensions to install (2-5 minutes)

### Using VS Code Tasks

After workspace is open:

1. Press `Ctrl+Shift+P`
2. Type: "Tasks: Run Task"
3. Choose:
   - "Docker: Up" - Start services
   - "Docker: Logs" - View logs
   - "Docker: Status" - Check status
   - "Health Check" - Test API
   - "Validate Setup" - Run validation

---

## What to Do After Startup

### 📚 Immediate (5 minutes)

- [ ] Read QUICKSTART.md (first steps guide)
- [ ] Test API at http://localhost:8000/docs
- [ ] Create test user and conversation
- [ ] Review SETUP_COMPLETE.md for overview

### 🔧 Short Term (30 minutes)

- [ ] Read DEVELOPMENT.md (coding guide)
- [ ] Explore project structure in VS Code
- [ ] Review `app/main.py` - entry point
- [ ] Check database with: `docker-compose exec db psql -U chatuser -d chatdb`

### 📖 Medium Term (Before Development)

- [ ] Read README.md - full project docs
- [ ] Read DEVELOPMENT.md - all development info
- [ ] Review app/models/ - database models
- [ ] Review app/routes/ - API endpoints
- [ ] Review app/services/ - business logic

### 🚀 Before Production

- [ ] Read SECURITY.md - hardening
- [ ] Read DEPLOYMENT.md - production setup
- [ ] Configure OPENAI_API_KEY in .env
- [ ] Update database passwords
- [ ] Review all configuration

---

## Useful Commands Reference

### View Status
```powershell
docker-compose ps                    # Service status
docker-compose logs -f               # Live logs
docker-compose logs -f app           # App logs only
```

### Manage Services
```powershell
docker-compose start                 # Start stopped services
docker-compose stop                  # Stop (keep data)
docker-compose restart               # Restart
docker-compose down                  # Stop & remove containers
docker-compose down -v               # Also delete volumes (⚠️ data lost)
```

### Database
```powershell
docker-compose exec db psql -U chatuser -d chatdb    # PostgreSQL shell
docker-compose exec cache redis-cli                   # Redis shell
```

### API Testing
```powershell
curl http://localhost:8000/health    # Health check
curl http://localhost:8000/docs      # API docs
```

---

## ✅ Ready to Start!

### Checklist Before Starting

- [ ] All pre-startup checklist items done
- [ ] `.env` file created
- [ ] Docker running
- [ ] Correct directory: `C:\Users\Akanksha Singh\Downloads\ai chat`

### Let's Start!

```powershell
# 1. Validate
python scripts/validate_setup.py

# 2. Start services
docker-compose up -d

# 3. Wait 30 seconds

# 4. Health check
curl http://localhost:8000/health

# 5. Open browser
# Visit: http://localhost:8000/docs

# 🎉 You're running!
```

---

## 🎯 Next Steps

1. ✅ Follow startup steps above
2. ✅ Test API at http://localhost:8000/docs
3. ✅ Read QUICKSTART.md for detailed guide
4. ✅ Read DEVELOPMENT.md for deep dive
5. ✅ Start building! 🚀

---

## 📞 Need Help?

| Problem | Solution |
|---------|----------|
| Services won't start | `docker-compose logs` then check QUICKSTART.md |
| API not responding | Wait 30 seconds, then try health check |
| Port in use | Change port in docker-compose.yml |
| Database error | `docker-compose restart db` |
| Need to rebuild | `docker-compose build --no-cache` |

---

## Status Indicators

| Indicator | Meaning | Action |
|-----------|---------|--------|
| ✅ green | All good | Continue |
| ⚠️ yellow | Warning | Review logs |
| ❌ red | Error | Check QUICKSTART.md troubleshooting |

---

**You're all set! Start with: `docker-compose up -d` 🚀**
