# Security Configuration Guide

## 🔐 Overview

This guide covers security setup and best practices for the Smart Chat API.

## SSL/TLS Configuration

### Development Setup (Self-signed Certificates)

Self-signed certificates are automatically created during setup:

```bash
cd nginx/ssl
ls -la  # View certificate files
```

### Production Setup (Let's Encrypt)

#### Prerequisites
- Domain name pointing to your server
- Port 80 and 443 accessible from internet

#### Steps

1. **Install Certbot**
```bash
sudo apt-get install certbot python3-certbot-nginx
```

2. **Obtain Certificate**
```bash
sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com
```

3. **Copy Certificates to Project**
```bash
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem nginx/ssl/cert.pem
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem nginx/ssl/key.pem
sudo chown $USER:$USER nginx/ssl/*.pem
```

4. **Update NGINX Configuration**

Edit `nginx/nginx.conf` and update:
```nginx
server_name yourdomain.com www.yourdomain.com;
ssl_certificate /etc/nginx/ssl/cert.pem;
ssl_certificate_key /etc/nginx/ssl/key.pem;
```

5. **Auto-renewal with Certbot**
```bash
# Add to crontab
0 12 * * * certbot renew --quiet --post-hook "cd /path/to/project && docker-compose restart nginx"
```

## 🔑 Secret Management

### Environment Variables

**Never commit `.env` file to version control!**

```bash
# Ensure .env is in .gitignore
echo ".env" >> .gitignore

# Use strong random values
openssl rand -hex 32  # Generate SECRET_KEY
```

### GitHub Secrets Setup

For CI/CD deployments, configure GitHub secrets:

1. Go to Repository Settings → Secrets and Variables → Actions
2. Add secrets:
   - `DEPLOY_KEY`: SSH private key for deployment
   - `DEPLOY_HOST`: Server hostname
   - `DEPLOY_USER`: SSH username
   - `DEPLOY_PATH`: Deployment directory

### Production Values

Generate strong secrets for production:

```python
import secrets
import string

# Generate SECRET_KEY
key = secrets.token_urlsafe(32)
print(f"SECRET_KEY={key}")

# Generate database password
db_pass = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(16))
print(f"DB_PASSWORD={db_pass}")

# Generate Redis password
redis_pass = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(16))
print(f"REDIS_PASSWORD={redis_pass}")
```

## 🔐 Authentication & Authorization

### JWT Configuration

Default token expiration: 30 minutes

Update in `app/config.py`:
```python
ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # Adjust as needed
```

### Password Requirements

Passwords are hashed using bcrypt with 12 rounds (default).

To adjust:
```python
# In app/models/user.py
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", rounds=14)
```

### API Key Management

For production, consider implementing:
- API key rotation
- Scoped permissions
- Usage quotas

## 🛡️ Rate Limiting

Current configuration in `nginx/nginx.conf`:

```nginx
limit_req_zone $binary_remote_addr zone=general:10m rate=10r/s;
limit_req_zone $binary_remote_addr zone=auth:10m rate=5r/m;
```

Adjust rates based on your needs:
```nginx
# Allow 20 requests per second
limit_req_zone $binary_remote_addr zone=general:10m rate=20r/s;

# Allow 10 login attempts per minute
limit_req_zone $binary_remote_addr zone=auth:10m rate=10r/m;
```

## 🚨 Security Headers

Configured in `nginx/nginx.conf`:

```nginx
# Prevent clickjacking
add_header X-Frame-Options "SAMEORIGIN" always;

# Prevent MIME type sniffing
add_header X-Content-Type-Options "nosniff" always;

# Enable XSS protection
add_header X-XSS-Protection "1; mode=block" always;

# Content Security Policy (customize as needed)
add_header Content-Security-Policy "default-src 'self'" always;
```

Add additional headers for specific needs:
```nginx
# HSTS (enforce HTTPS)
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

# Prevent referrer leakage
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
```

## 🔒 Container Security

### Non-root User

All containers run as non-root by default:

```dockerfile
# Dockerfile - already configured
RUN useradd -m -u 1000 appuser
USER appuser
```

### Resource Limits

Add to `docker-compose.yml`:

```yaml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
```

### Volume Permissions

Ensure proper permissions:

```bash
# Database volume
chmod 755 /var/lib/postgresql/data

# Redis volume
chmod 755 /var/lib/redis/data
```

## 🗄️ Database Security

### PostgreSQL

#### Strong Credentials
```bash
# Generate strong password
openssl rand -base64 32 | tr -d '=' | cut -c1-20
```

#### Connection Security
- ✅ Change default credentials in `.env`
- ✅ Restrict network access (only from app container)
- ✅ Enable SSL connections (if external)

#### Backup Security
```bash
# Backup with encryption
docker-compose exec db pg_dump -U chatuser chatdb | \
  gpg --symmetric --cipher-algo AES256 > backup.sql.gpg
```

### Redis

#### Enable Authentication
```yaml
# docker-compose.yml
cache:
  command: redis-server --requirepass ${REDIS_PASSWORD}
```

#### Disable Dangerous Commands
```redis
rename-command FLUSHDB ""
rename-command FLUSHALL ""
rename-command KEYS ""
```

## 🔍 Monitoring & Logging

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f app

# With timestamps
docker-compose logs -f --timestamps app
```

### Access Logs

NGINX access logs location:
```bash
docker-compose exec nginx cat /var/log/nginx/access.log
```

## 🔐 CORS Configuration

Current settings in `app/config.py`:

```python
CORS_ORIGINS: list = [
    "http://localhost",
    "http://localhost:3000",
    "https://yourdomain.com",
]
```

**For production:**
```python
# Only allow specific domains
CORS_ORIGINS: list = [
    "https://yourdomain.com",
    "https://www.yourdomain.com",
]
```

## ✅ Security Checklist

- [ ] Update SECRET_KEY in `.env`
- [ ] Generate strong database passwords
- [ ] Generate strong Redis password
- [ ] Set `DEBUG=False` in `.env`
- [ ] Update CORS origins for your domain
- [ ] Configure SSL certificates (Let's Encrypt)
- [ ] Set resource limits in docker-compose.yml
- [ ] Enable HSTS header for HTTPS
- [ ] Configure backup strategy for databases
- [ ] Set up monitoring and alerting
- [ ] Regular security updates: `docker-compose pull`
- [ ] Review and audit logs regularly
- [ ] Implement API rate limiting per user/IP
- [ ] Use strong JWT expiration times
- [ ] Enable HTTPS only (redirect HTTP)

## 🚨 Incident Response

### If API Key is Compromised
1. Immediately revoke the key
2. Regenerate SECRET_KEY in `.env`
3. Restart app: `docker-compose restart app`
4. Audit access logs for unauthorized usage

### If Database is Compromised
1. Stop services: `docker-compose stop`
2. Change database password in `.env`
3. Check backups for integrity
4. Restore from clean backup if needed
5. Restart services: `docker-compose up -d`

### Regular Backups

```bash
#!/bin/bash
# backup.sh - Automated backup script

BACKUP_DIR="./backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

mkdir -p $BACKUP_DIR

# PostgreSQL backup
docker-compose exec -T db pg_dump -U chatuser chatdb | \
  gzip > $BACKUP_DIR/db_backup_$TIMESTAMP.sql.gz

# Keep only last 7 days
find $BACKUP_DIR -name "db_backup_*.sql.gz" -mtime +7 -delete
```

Schedule with cron:
```bash
0 2 * * * /path/to/project/backup.sh
```

## 📚 References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Docker Security Best Practices](https://docs.docker.com/engine/security/)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [PostgreSQL Security](https://www.postgresql.org/docs/current/sql-syntax.html)
- [NGINX Security Headers](https://nginx.org/en/docs/http/ngx_http_headers_module.html)

---

Stay secure! 🔐
