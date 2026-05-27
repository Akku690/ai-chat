# 🎯 Production Keys Quick Reference

## 📌 For Production Deployment - Get Started Here

Created: **PRODUCTION_KEYS_GUIDE.md** - Comprehensive guide for all production keys and credentials.

---

## 🔑 ALL REQUIRED KEYS FOR PRODUCTION

### 1. **SECRET_KEY** (Critical)
```
What: Cryptographic key for JWT tokens
Generate: python -c "import secrets; print(secrets.token_urlsafe(64))"
Length: 64+ characters (very random)
Change: Every 12 months
```

### 2. **DB_USER** (Critical)
```
What: PostgreSQL database username
Example: prod_chat_app_user
Length: 12+ characters, alphanumeric + underscore only
Change: Once during setup
```

### 3. **DB_PASSWORD** (Critical)
```
What: PostgreSQL database password
Generate: python -c "import secrets; print(secrets.token_urlsafe(32))"
Length: 32+ characters
Mix: Uppercase, lowercase, numbers, special chars
Change: Every 6 months
```

### 4. **REDIS_PASSWORD** (High)
```
What: Redis cache authentication password
Generate: python -c "import secrets; print(secrets.token_urlsafe(32))"
Length: 32+ characters
Change: Every 6 months
```

### 5. **SSL_CERT** & **SSL_KEY** (Critical)
```
What: HTTPS security certificates
How: Use Let's Encrypt (FREE)
Steps: See PRODUCTION_KEYS_GUIDE.md section 4
Renewal: Automatic (every 90 days)
```

### 6. **OPENAI_API_KEY** (Optional)
```
What: API key for ChatGPT integration
Required: NO - app works without it
Get: https://platform.openai.com/api/keys
Cost: Usually under $1/month
Change: Every 6 months
```

### 7. **DB_BACKUP_PASSWORD** (High)
```
What: Secure database backup password
Generate: python -c "import secrets; print(secrets.token_urlsafe(32))"
Used: For encrypted database backups
Change: Every 6 months
```

---

## 🚀 Quick Generation Commands

Copy-paste these in PowerShell to generate all keys instantly:

```powershell
# SECRET_KEY (64 char)
Write-Host "SECRET_KEY:"
python -c "import secrets; print(secrets.token_urlsafe(64))"

# DB_PASSWORD (32 char)
Write-Host "DB_PASSWORD:"
python -c "import secrets; print(secrets.token_urlsafe(32))"

# REDIS_PASSWORD (32 char)
Write-Host "REDIS_PASSWORD:"
python -c "import secrets; print(secrets.token_urlsafe(32))"

# DB_BACKUP_PASSWORD (32 char)
Write-Host "DB_BACKUP_PASSWORD:"
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## 📋 Production .env.prod Template

```env
# APPLICATION
DEBUG=False
ENVIRONMENT=production
SECRET_KEY=<copy-64-char-key-here>

# DATABASE
DB_HOST=your-db-server.com
DB_PORT=5432
DB_USER=prod_chat_app_user
DB_PASSWORD=<copy-32-char-password-here>
DB_NAME=chatdb_prod
DB_BACKUP_PASSWORD=<copy-32-char-backup-password-here>

# REDIS
REDIS_HOST=your-redis-server.com
REDIS_PORT=6379
REDIS_PASSWORD=<copy-32-char-password-here>

# SSL/HTTPS
SSL_CERT_PATH=/etc/letsencrypt/live/yourdomain.com/fullchain.pem
SSL_KEY_PATH=/etc/letsencrypt/live/yourdomain.com/privkey.pem
FORCE_HTTPS=True

# SECURITY
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,api.yourdomain.com
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# AI (OPTIONAL)
OPENAI_API_KEY=sk-proj-<optional-production-key>

# MONITORING
LOG_LEVEL=INFO
```

---

## ✅ STEP-BY-STEP PRODUCTION SETUP

### Phase 1: Generate Keys (10 minutes)
```
1. Run commands above in PowerShell
2. Copy all generated keys
3. Save in password manager (CRITICAL!)
```

### Phase 2: SSL Certificate (10 minutes)
```
1. Use Let's Encrypt (FREE, automatic renewal)
2. Command: sudo certbot certonly --standalone -d yourdomain.com
3. Certificates saved to: /etc/letsencrypt/live/yourdomain.com/
```

### Phase 3: Create .env.prod (5 minutes)
```
1. Copy template above
2. Replace all placeholders with generated keys
3. Replace domain names with your actual domain
4. Save as .env.prod on server
5. Set permissions: chmod 600 .env.prod
```

### Phase 4: Deploy (10 minutes)
```
1. Copy .env.prod to server: scp .env.prod user@server:~/
2. Deploy: docker-compose --env-file .env.prod up -d
3. Verify: curl https://yourdomain.com/health
```

### Phase 5: Monitor (Ongoing)
```
1. Check logs: docker-compose logs app
2. Monitor errors: Set up Sentry (free)
3. Review usage: Weekly check
```

---

## 🔐 Security Rules (MUST FOLLOW)

### ✅ DO
- ✅ Use 64+ character SECRET_KEY
- ✅ Use 32+ character passwords
- ✅ Mix case, numbers, special chars
- ✅ Use Let's Encrypt SSL (free)
- ✅ Store in password manager
- ✅ Rotate keys every 6-12 months
- ✅ Add .env.prod to .gitignore
- ✅ Use chmod 600 on .env.prod file
- ✅ Keep backups of credentials
- ✅ Monitor SSL expiration dates

### ❌ DON'T
- ❌ Use simple passwords
- ❌ Reuse keys across environments
- ❌ Share via email/Slack
- ❌ Commit to Git
- ❌ Hardcode in source code
- ❌ Use test credentials in production
- ❌ Skip SSL/HTTPS
- ❌ Expose SECRET_KEY in logs
- ❌ Use same key for multiple environments

---

## 📊 Key Rotation Schedule

```
Every 3 months:  OPENAI_API_KEY
Every 6 months:  DB_PASSWORD, REDIS_PASSWORD, DB_BACKUP_PASSWORD
Every 12 months: SECRET_KEY
As needed:       SSL (automatic with Let's Encrypt)
```

---

## 📂 Complete Documentation

| File | Purpose |
|------|---------|
| **PRODUCTION_KEYS_GUIDE.md** | Full production setup guide |
| KEYS_GUIDE.md | Development keys guide |
| DEPLOYMENT.md | General deployment steps |
| SECURITY.md | Security best practices |
| CI_CD_SETUP.md | Automated deployment |

---

## 🆘 Troubleshooting

### Can't connect to database?
```powershell
# Check credentials in .env.prod
cat .env.prod | grep DB_

# Test connection from server
psql -h your-db-host -U prod_chat_app_user -d chatdb_prod
```

### SSL certificate not working?
```bash
# Check certificate validity
openssl x509 -in /etc/letsencrypt/live/yourdomain.com/fullchain.pem -noout -dates

# Renew if needed
sudo certbot renew
```

### Can't access API?
```bash
# Check service status
docker-compose ps

# View logs
docker-compose logs app
docker-compose logs nginx
```

---

## 🎯 Total Time Estimate

| Task | Time |
|------|------|
| Generate keys | 10 min |
| Create SSL cert | 10 min |
| Create .env.prod | 5 min |
| Deploy app | 10 min |
| Test endpoints | 10 min |
| **TOTAL** | **45 min** |

---

## 📞 Need Help?

- **Production Setup**: See PRODUCTION_KEYS_GUIDE.md
- **Development**: See KEYS_GUIDE.md
- **Deployment**: See DEPLOYMENT.md
- **Security**: See SECURITY.md

---

## ✨ You're Ready!

1. Generate keys (10 min)
2. Get SSL certificate (10 min)
3. Create .env.prod file (5 min)
4. Deploy to production (10 min)
5. Monitor and maintain

**Follow PRODUCTION_KEYS_GUIDE.md for detailed step-by-step instructions!** 🚀
