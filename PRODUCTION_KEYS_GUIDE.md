# 🔐 Production Keys Guide - Complete Setup

This guide covers all keys required for **production deployment** with security best practices.

---

## 📋 Production Requirements Summary

| Key | Required | Importance | Where Used |
|-----|----------|-----------|-----------|
| **SECRET_KEY** | ✅ Yes | 🔴 Critical | JWT tokens, sessions |
| **DB_USER** | ✅ Yes | 🔴 Critical | PostgreSQL access |
| **DB_PASSWORD** | ✅ Yes | 🔴 Critical | PostgreSQL access |
| **REDIS_PASSWORD** | ✅ Yes | 🟠 High | Redis authentication |
| **OPENAI_API_KEY** | ❌ Optional | 🟢 Low | AI responses |
| **DJANGO_ALLOWED_HOSTS** | ✅ Yes | 🟠 High | Security (CORS) |
| **SSL_CERT** | ✅ Yes | 🔴 Critical | HTTPS |
| **SSL_KEY** | ✅ Yes | 🔴 Critical | HTTPS |
| **DB_BACKUP_PASSWORD** | ✅ Yes | 🟠 High | Database backups |

---

## 🚀 Production Environment File

Create a **production `.env.prod`** file with these values:

```env
# ============================================
# PRODUCTION ENVIRONMENT CONFIGURATION
# ============================================

# ============================================
# 1. APPLICATION SETTINGS
# ============================================
DEBUG=False
ENVIRONMENT=production
SECRET_KEY=<generate-new-64-char-key>

# ============================================
# 2. DATABASE CONFIGURATION
# ============================================
DB_HOST=your-db-server.com
DB_PORT=5432
DB_USER=<strong-username-16-chars>
DB_PASSWORD=<strong-password-32-chars>
DB_NAME=chatdb_prod
DB_POOL_SIZE=20
DB_MAX_OVERFLOW=40
DB_BACKUP_PASSWORD=<backup-password-32-chars>

# ============================================
# 3. REDIS CACHE
# ============================================
REDIS_HOST=your-redis-server.com
REDIS_PORT=6379
REDIS_PASSWORD=<strong-password-32-chars>
REDIS_DB=0
REDIS_SSL=True
REDIS_SSL_CERT_REQS=required

# ============================================
# 4. SECURITY & HTTPS
# ============================================
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,api.yourdomain.com
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
SSL_CERT_PATH=/etc/letsencrypt/live/yourdomain.com/fullchain.pem
SSL_KEY_PATH=/etc/letsencrypt/live/yourdomain.com/privkey.pem
FORCE_HTTPS=True
HSTS_MAX_AGE=31536000

# ============================================
# 5. AI INTEGRATION (OPTIONAL)
# ============================================
OPENAI_API_KEY=sk-proj-<your-production-key>
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_REQUEST_TIMEOUT=30

# ============================================
# 6. LOGGING & MONITORING
# ============================================
LOG_LEVEL=INFO
SENTRY_DSN=https://<your-sentry-key>@sentry.io/<project-id>

# ============================================
# 7. EMAIL NOTIFICATIONS (OPTIONAL)
# ============================================
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=<your-email>
SMTP_PASSWORD=<app-password>
ADMIN_EMAIL=admin@yourdomain.com
```

---

# 🔑 STEP-BY-STEP: Generate Production Keys

## 1️⃣ SECRET_KEY (Critical)

### What it does
- Signs JWT tokens
- Secures session cookies
- **MUST be random and unique**
- **MUST be 64+ characters**

### Generate (Choose ONE method)

#### Method 1: Python (Recommended)
```powershell
# Windows PowerShell
python -c "import secrets; print(secrets.token_urlsafe(64))"

# Output example:
# SWpKazU3M3lOdW9vN3dKaTRkTFFJdjVENkJkSmlKWVUyTGZWMDlzTkdjeFJ6RTJNREkyVFhNeVEzQTNSRFJCTVRoRmVRPT0=
```

#### Method 2: Python (More Random)
```powershell
python -c "import os; print(os.urandom(64).hex())"

# Output example:
# a7f8c2e5b1d6f9e3a4c7b8d1f6e9c2a5b8d1e4f7a0b3c6d9e2f5a8b1c4d7e0f3a6b9c2d5e8f1a4b7c0d3e6f9a2b5c8d1e4f7a0b3c
```

#### Method 3: OpenSSL
```powershell
# Windows PowerShell
certutil -encodehex -f -nologo <(Get-Random -InputObject (0..255) -Count 64) | Select -Last 1

# Or use online tool: https://randomkeygen.com/
# Copy from "Fort Knox Passwords" section
```

### Store it
```powershell
# Save to .env.prod
$key = "SWpKazU3M3lOdW9vN3dKaTRkTFFJdjVENkJkSmlKWVUyTGZWMDlzTkdjeFJ6RTJNREkyVFhNeVEzQTNSRFJCTVRoRmVRPT0="
Add-Content .env.prod "SECRET_KEY=$key"
```

---

## 2️⃣ DATABASE CREDENTIALS (Critical)

### DB_USER

**Requirements**:
- 12-16 characters minimum
- Alphanumeric + underscore only
- No spaces or special characters
- Different from default

### Generate Strong Username
```powershell
# Option 1: Custom name
# prod_chat_user_2024

# Option 2: Random
python -c "import secrets; print('db_' + secrets.token_hex(8))"
# Output: db_f7a8c2e5b1d6f9e3

# Recommended: Use meaningful but secure
$dbUser = "prod_chat_app_user"
```

### DB_PASSWORD

**Requirements**:
- 32+ characters minimum
- Mix: uppercase, lowercase, numbers, special chars
- Avoid common patterns
- Different for each environment

### Generate Strong Password
```powershell
# Option 1: Python (Recommended)
python -c "import secrets; print(secrets.token_urlsafe(32))"
# Output: xY2q_mK8pL5vJ9nW_3B_aZ1c_dF4eR_sT

# Option 2: PowerShell
$chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()'
$password = -join ((Get-Random -InputObject $chars.ToCharArray() -Count 32))
$password

# Option 3: Online generator (if needed)
# https://www.random.org/passwords/

# Recommended format for production:
# Prod_Chat_Db_P@ssw0rd_2024_Secure_Key_12345
```

### Store it
```powershell
# Add to .env.prod
$dbPass = "xY2q_mK8pL5vJ9nW_3B_aZ1c_dF4eR_sT"
Add-Content .env.prod "DB_PASSWORD=$dbPass"
```

### Test Connection
```powershell
# After deploying, test database connection:
psql -h your-db-server.com -U prod_chat_app_user -d chatdb_prod -c "SELECT 1"

# You'll be prompted for password
```

---

## 3️⃣ REDIS_PASSWORD (High Priority)

### Requirements
- 32+ characters
- Strong random string
- Different from DB_PASSWORD

### Generate
```powershell
# Python
python -c "import secrets; print(secrets.token_urlsafe(32))"
# Output: aT7r_mN2pQ9sK4wX_8L_bF3gH_jD5vB

# Store in .env.prod
Add-Content .env.prod "REDIS_PASSWORD=aT7r_mN2pQ9sK4wX_8L_bF3gH_jD5vB"
```

### Test Connection
```powershell
# After deploying:
redis-cli -h your-redis-server.com -a aT7r_mN2pQ9sK4wX_8L_bF3gH_jD5vB ping
# Expected output: PONG
```

---

## 4️⃣ SSL CERTIFICATE & KEY (Critical for HTTPS)

### Option A: Let's Encrypt (FREE - Recommended)

#### Step 1: Install Certbot
```powershell
# On Linux/Ubuntu server:
sudo apt-get install certbot python3-certbot-nginx

# On Windows (if running on Windows):
# Download from: https://certbot.eff.org/instructions?os=windows
```

#### Step 2: Generate Certificate
```powershell
# On your server:
sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com

# You'll be asked:
# - Email address
# - Accept terms
# - Agree to share email

# Certificates saved to:
# /etc/letsencrypt/live/yourdomain.com/
```

#### Step 3: Add to .env.prod
```env
SSL_CERT_PATH=/etc/letsencrypt/live/yourdomain.com/fullchain.pem
SSL_KEY_PATH=/etc/letsencrypt/live/yourdomain.com/privkey.pem
```

#### Step 4: Auto-Renew
```powershell
# Certificates expire after 90 days
# Set up automatic renewal:
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer

# Check status:
sudo systemctl status certbot.timer
```

---

### Option B: Self-Signed (Development/Testing Only)

⚠️ **NOT for production** - browsers will warn users

```powershell
# Generate on Windows:
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365

# Fill in prompts:
# Country: US
# State: CA
# City: San Francisco
# Organization: Your Company
# Common Name: yourdomain.com

# Copy to server:
scp cert.pem user@server:/etc/nginx/ssl/
scp key.pem user@server:/etc/nginx/ssl/

# Add to .env.prod:
SSL_CERT_PATH=/etc/nginx/ssl/cert.pem
SSL_KEY_PATH=/etc/nginx/ssl/key.pem
```

---

### Option C: Paid SSL Certificate

1. Purchase from:
   - Comodo: https://www.comodosslcertificates.com/
   - Digicert: https://www.digicert.com/
   - Others: Any reputable provider

2. Follow provider's installation guide

3. Add paths to .env.prod

---

## 5️⃣ OPENAI_API_KEY (Optional)

### If You Want AI Features in Production

#### Step 1: Create Separate Production Key
```
⚠️ MUST be different from development key
```

#### Step 2: Get Production API Key
1. Log in to: https://platform.openai.com/account/api-keys
2. Click "Create new secret key"
3. Name it: `Smart-Chat-AI-Production`
4. Copy immediately
5. Save in password manager

#### Step 3: Set Usage Limits
```
1. Go to: https://platform.openai.com/account/billing/overview
2. Set "Hard limit" to: $100 (your budget)
3. Set "Soft limit" to: $80 (alert threshold)
4. Save
```

#### Step 4: Add to .env.prod
```env
OPENAI_API_KEY=sk-proj-<your-production-key>
```

#### Step 5: Monitor Usage
- Weekly: Check OpenAI dashboard
- Monthly: Review costs
- Quarterly: Optimize prompts if needed

---

## 6️⃣ ADDITIONAL PRODUCTION KEYS

### DB_BACKUP_PASSWORD

For secure database backups:

```powershell
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Add to .env.prod
Add-Content .env.prod "DB_BACKUP_PASSWORD=<generated-password>"
```

### SENTRY_DSN (Error Monitoring)

1. Go to: https://sentry.io/auth/login/
2. Create free account
3. Create new project → Python
4. Copy DSN: `https://<key>@sentry.io/<project-id>`
5. Add to .env.prod:
   ```env
   SENTRY_DSN=https://<key>@sentry.io/<project-id>
   ```

---

## 📋 Complete Production Checklist

### Before Deployment

- [ ] **SECRET_KEY** - Generated new 64+ char key
- [ ] **DB_USER** - Set to strong username (12+ chars)
- [ ] **DB_PASSWORD** - Generated 32+ char password
- [ ] **REDIS_PASSWORD** - Generated 32+ char password
- [ ] **SSL_CERT_PATH** - Path to SSL certificate
- [ ] **SSL_KEY_PATH** - Path to SSL private key
- [ ] **ALLOWED_HOSTS** - Set to your domain
- [ ] **CORS_ORIGINS** - Set to your domain only
- [ ] **DEBUG** - Set to `False`
- [ ] **ENVIRONMENT** - Set to `production`
- [ ] **.env.prod created** - In secure location
- [ ] **All credentials backed up** - In password manager
- [ ] **Keys not in Git** - Add .env.prod to .gitignore
- [ ] **SSL certificates valid** - Check expiration dates
- [ ] **Database tested** - Connection verified
- [ ] **Redis tested** - Connection verified

### Deployment

- [ ] Copy `.env.prod` to server (secure method)
- [ ] Set file permissions: `chmod 600 .env.prod`
- [ ] Update docker-compose to use `.env.prod`
- [ ] Run migrations
- [ ] Start containers
- [ ] Test all endpoints
- [ ] Monitor logs for errors
- [ ] Set up monitoring/alerts

### Post-Deployment

- [ ] Monitor error logs daily
- [ ] Check SSL certificate expiration (renew 30 days before)
- [ ] Review database backups
- [ ] Monitor API usage/costs
- [ ] Test disaster recovery quarterly
- [ ] Rotate keys annually

---

## 🔐 Security Best Practices for Production

### ✅ DO

- [x] **Use environment variables** for all secrets
- [x] **Rotate keys annually** - especially SECRET_KEY
- [x] **Use strong passwords** - 32+ characters, mixed case
- [x] **Enable SSL/TLS** - always use HTTPS
- [x] **Use separate credentials** for each environment
- [x] **Store backups** of credentials in secure location
- [x] **Use password manager** for credential management
- [x] **Implement rate limiting** - protect API endpoints
- [x] **Enable logging** - track all access attempts
- [x] **Use VPN/firewall** - restrict database access
- [x] **Monitor API usage** - detect unusual activity
- [x] **Set spending limits** - for OpenAI account

### ❌ DON'T

- [ ] **Never hardcode secrets** in code
- [ ] **Never commit .env.prod** to Git
- [ ] **Never use test/default credentials** in production
- [ ] **Never share credentials** via email/Slack
- [ ] **Never reuse passwords** across services
- [ ] **Never use same key** for multiple environments
- [ ] **Never expose SECRET_KEY** in logs
- [ ] **Never skip SSL** - even for internal services
- [ ] **Never disable security headers** for convenience
- [ ] **Never store credentials** in plaintext files
- [ ] **Never use simple passwords** like "password123"

---

## 🚀 Deployment Process

### Step 1: Prepare Credentials
```powershell
# Generate all keys
$secretKey = "python -c import secrets; print(secrets.token_urlsafe(64))"
$dbPassword = "python -c import secrets; print(secrets.token_urlsafe(32))"
$redisPassword = "python -c import secrets; print(secrets.token_urlsafe(32))"

# Create .env.prod with all values
```

### Step 2: Create Secrets on Server
```bash
# SSH into your production server
ssh user@yourdomain.com

# Create .env.prod securely
# Option 1: Copy from secure file transfer
scp .env.prod user@yourdomain.com:~/

# Option 2: Create on server directly
nano /home/user/.env.prod
# Paste contents and save (Ctrl+O, Enter, Ctrl+X)

# Set permissions (critical!)
chmod 600 /home/user/.env.prod
```

### Step 3: Deploy Application
```bash
# SSH to server
ssh user@yourdomain.com

# Navigate to project
cd /opt/smart-chat-ai

# Copy .env.prod to app directory
sudo cp ~/.env.prod /opt/smart-chat-ai/.env.prod

# Update docker-compose
docker-compose -f docker-compose.yml --env-file .env.prod up -d

# Verify services
docker-compose ps
```

### Step 4: Verify Deployment
```bash
# Check health
curl https://yourdomain.com/health

# Check logs
docker-compose logs app
docker-compose logs db
docker-compose logs nginx

# Test API
curl -X POST https://yourdomain.com/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!"}'
```

---

## 📊 Production Environment Comparison

| Item | Development | Production |
|------|-------------|-----------|
| **DEBUG** | True | False |
| **SECRET_KEY** | Can be simple | Must be 64+ random chars |
| **DB_PASSWORD** | "chatpass" | 32+ strong random |
| **REDIS_PASSWORD** | "redispass" | 32+ strong random |
| **SSL** | Self-signed OK | Let's Encrypt required |
| **Backups** | Optional | Daily required |
| **Monitoring** | Basic | Comprehensive |
| **Rate Limiting** | Disabled | Enabled |
| **Logs** | Verbose | INFO level |
| **CORS** | Open | Restricted to domain |

---

## 🆘 Troubleshooting

### Problem: Connection refused (database)
```bash
# Check credentials in .env.prod
cat .env.prod | grep DB_

# Test connection
psql -h your-db-host -U $DB_USER -d chatdb_prod

# Check database service
docker-compose logs db
```

### Problem: SSL certificate error
```bash
# Check certificate validity
openssl x509 -in /path/to/cert.pem -noout -dates

# Renew if needed (Let's Encrypt)
sudo certbot renew

# Restart nginx
docker-compose restart nginx
```

### Problem: Can't access API
```bash
# Check firewall
sudo ufw status

# Check NGINX config
docker-compose logs nginx

# Test locally
curl http://localhost:8000/health
```

### Problem: Out of memory
```bash
# Check resource usage
docker stats

# Increase limits in docker-compose.yml
services:
  app:
    deploy:
      resources:
        limits:
          memory: 2G
```

---

## 📞 Key Rotation Schedule

```
Every 3 months:  OPENAI_API_KEY
Every 6 months:  DB_PASSWORD, REDIS_PASSWORD
Every 12 months: SECRET_KEY
As needed:       SSL certificates (Let's Encrypt auto-renews)
```

---

## ✅ Summary

**Keys Required for Production:**
1. ✅ **SECRET_KEY** - 64+ random characters
2. ✅ **DB_USER** - 12+ characters, unique
3. ✅ **DB_PASSWORD** - 32+ strong random
4. ✅ **REDIS_PASSWORD** - 32+ strong random
5. ✅ **SSL_CERT** - Let's Encrypt (free)
6. ✅ **SSL_KEY** - Let's Encrypt (free)
7. ❌ **OPENAI_API_KEY** - Optional (for AI)

**Total Setup Time:** 30-60 minutes

**Critical Steps:**
1. Generate all credentials securely
2. Set up Let's Encrypt SSL
3. Test all connections before deploying
4. Monitor after deployment
5. Set up key rotation schedule

---

## 🎯 Ready for Production!

All keys are generated securely, connections are tested, and deployment is ready.

**Next Step**: Deploy to production server following the deployment process above.

Questions? Check KEYS_GUIDE.md for additional details.
