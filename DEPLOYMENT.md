# Deployment Guide

## 🚀 Production Deployment

This guide covers deploying the Smart Chat API to production.

## Prerequisites

### Server Requirements

- Ubuntu 20.04 LTS or newer
- Minimum 2GB RAM (4GB recommended)
- 10GB disk space
- Docker and Docker Compose installed
- Domain name with DNS configured
- SSH access to server

### Server Setup

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Add user to docker group (optional but recommended)
sudo usermod -aG docker $USER
newgrp docker

# Verify installation
docker --version
docker-compose --version
```

## 📁 Directory Structure

```bash
# Create project directory
sudo mkdir -p /opt/smart-chat-ai
cd /opt/smart-chat-ai

# Create subdirectories
sudo mkdir -p {nginx/ssl,scripts,backups,.github/workflows}
```

## 🔧 Configuration

### 1. Copy Project Files

```bash
# Copy from local machine or clone from GitHub
git clone https://github.com/yourusername/smart-chat-ai.git /opt/smart-chat-ai
cd /opt/smart-chat-ai
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with production values
sudo nano .env
```

**Critical production settings:**

```env
DEBUG=False
SECRET_KEY=<generate-new-secure-key>
DB_USER=chatuser
DB_PASSWORD=<generate-strong-password>
DB_NAME=chatdb
REDIS_PASSWORD=<generate-strong-password>
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-3.5-turbo
```

### 3. SSL Certificates

Option A: Let's Encrypt (Recommended)

```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot certonly --standalone \
  -d yourdomain.com \
  -d www.yourdomain.com

# Copy to project
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem nginx/ssl/cert.pem
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem nginx/ssl/key.pem
sudo chown -R $USER:$USER nginx/ssl/
```

Option B: Self-signed (Testing Only)

```bash
mkdir -p nginx/ssl
openssl req -x509 -newkey rsa:4096 \
  -keyout nginx/ssl/key.pem \
  -out nginx/ssl/cert.pem \
  -days 365 -nodes \
  -subj "/C=US/ST=State/L=City/O=Org/CN=yourdomain.com"
```

### 4. Update NGINX Configuration

Edit `nginx/nginx.conf`:

```nginx
server_name yourdomain.com www.yourdomain.com;
ssl_certificate /etc/nginx/ssl/cert.pem;
ssl_certificate_key /etc/nginx/ssl/key.pem;
```

## 🐳 Docker Deployment

### Build and Start Services

```bash
# Build images
docker-compose build

# Start services in background
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

### Health Check

```bash
# Wait for services to be ready
sleep 30

# Check health endpoint
curl -k https://localhost/health

# Expected response:
# {"status":"healthy","database":true,"redis":true,"ai_service":false}
```

## 🔄 Database Setup

### First Run Setup

```bash
# The database initializes automatically

# Verify database connection
docker-compose exec db psql -U chatuser -d chatdb -c "SELECT 1;"
```

### Backup Strategy

Create automated backup script:

```bash
#!/bin/bash
# /opt/smart-chat-ai/scripts/backup.sh

BACKUP_DIR="/opt/smart-chat-ai/backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Create backup directory
mkdir -p $BACKUP_DIR

# PostgreSQL backup
cd /opt/smart-chat-ai
docker-compose exec -T db pg_dump -U chatuser chatdb | \
  gzip > $BACKUP_DIR/db_backup_$TIMESTAMP.sql.gz

# Keep only last 30 days
find $BACKUP_DIR -name "db_backup_*.sql.gz" -mtime +30 -delete

# Sync to remote storage (optional)
# aws s3 sync $BACKUP_DIR s3://my-backups/

echo "Backup completed: $BACKUP_DIR/db_backup_$TIMESTAMP.sql.gz"
```

Make executable and schedule:

```bash
chmod +x scripts/backup.sh

# Add to crontab
(crontab -l; echo "0 2 * * * /opt/smart-chat-ai/scripts/backup.sh") | crontab -
```

## 🔐 Firewall & Security

### UFW (Uncomplicated Firewall)

```bash
# Enable UFW
sudo ufw enable

# Allow SSH (critical!)
sudo ufw allow 22/tcp

# Allow HTTP and HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Allow PostgreSQL (internal only)
sudo ufw allow from 172.17.0.0/16 to any port 5432

# Check status
sudo ufw status
```

### Network Configuration

```bash
# Update docker-compose.yml to restrict external access
services:
  db:
    ports:
      - "127.0.0.1:5432:5432"  # Only internal access

  cache:
    ports:
      - "127.0.0.1:6379:6379"  # Only internal access
```

## 🔄 SSL Auto-renewal

### Certbot Auto-renewal

```bash
# Test renewal
sudo certbot renew --dry-run

# Auto-renewal daemon
sudo systemctl start certbot.timer
sudo systemctl enable certbot.timer

# Check status
sudo systemctl status certbot.timer
```

### Restart NGINX After Renewal

Add to renewal hook:

```bash
sudo nano /etc/letsencrypt/renewal/yourdomain.com.conf
```

Add:
```
post_hook = /opt/smart-chat-ai/scripts/renew-cert.sh
```

Create hook script:

```bash
#!/bin/bash
# /opt/smart-chat-ai/scripts/renew-cert.sh

cd /opt/smart-chat-ai

# Copy certificates
cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem nginx/ssl/cert.pem
cp /etc/letsencrypt/live/yourdomain.com/privkey.pem nginx/ssl/key.pem

# Restart NGINX
docker-compose restart nginx

echo "SSL certificates renewed and NGINX restarted"
```

Make executable:
```bash
chmod +x scripts/renew-cert.sh
```

## 📊 Monitoring & Logging

### Container Logs

```bash
# View live logs
docker-compose logs -f

# View specific service
docker-compose logs -f app

# View last 100 lines
docker-compose logs --tail=100 app
```

### Log Rotation

Add to `/etc/logrotate.d/docker-compose`:

```
/opt/smart-chat-ai/logs/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 root docker
}
```

### Monitoring with Portainer (Optional)

```bash
# Deploy Portainer for web-based Docker management
docker run -d \
  --name portainer \
  --restart always \
  -p 9000:9000 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  portainer/portainer-ce:latest
```

Access at: `http://localhost:9000`

## 🚀 GitHub Actions CI/CD

### Setup Deployment Secrets

1. Go to GitHub Repository Settings
2. Navigate to Secrets and Variables → Actions
3. Add secrets:

```
DEPLOY_KEY        → SSH private key
DEPLOY_HOST       → yourdomain.com
DEPLOY_USER       → deploy_user
DEPLOY_PATH       → /opt/smart-chat-ai
```

### SSH Key Setup

```bash
# Generate SSH key on server
ssh-keygen -t rsa -b 4096 -f deploy_key

# Add to GitHub secrets (DEPLOY_KEY = private key content)

# Add public key to server authorized keys
cat deploy_key.pub >> ~/.ssh/authorized_keys
```

### GitHub Actions Workflow

The `.github/workflows/build-deploy.yml` file is already configured to:
1. Build Docker image on push
2. Run tests
3. Push to container registry
4. Deploy to production server

## 🔍 Troubleshooting

### Services Won't Start

```bash
# Check Docker daemon
sudo systemctl status docker

# View full logs
docker-compose logs

# Verify .env file
cat .env | grep SECRET_KEY
```

### Port Already in Use

```bash
# Find process using port
sudo lsof -i :80
sudo lsof -i :443

# Kill process
sudo kill -9 <PID>
```

### SSL Certificate Errors

```bash
# Verify certificate
openssl x509 -in nginx/ssl/cert.pem -text -noout

# Check expiration
openssl x509 -in nginx/ssl/cert.pem -noout -dates

# Force renewal
sudo certbot renew --force-renewal
```

### Database Connection Issues

```bash
# Test database connection
docker-compose exec app python -c \
  "from app.database import engine; engine.execute('SELECT 1')"

# Check database logs
docker-compose logs db
```

## 📈 Scaling

### Horizontal Scaling (Multiple App Instances)

```yaml
# docker-compose.yml
services:
  app:
    deploy:
      replicas: 3

  # Load balancer
  nginx:
    depends_on:
      - app_1
      - app_2
      - app_3
```

### Vertical Scaling (Resource Limits)

```yaml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G
```

## 🔐 Maintenance

### Regular Updates

```bash
# Update Docker images
docker-compose pull

# Rebuild and restart
docker-compose up -d --build
```

### Cleanup

```bash
# Remove unused images
docker image prune -a

# Remove unused volumes
docker volume prune

# Remove unused networks
docker network prune
```

### Restart Services

```bash
# Restart all services
docker-compose restart

# Restart specific service
docker-compose restart app

# Graceful shutdown and restart
docker-compose down
docker-compose up -d
```

## 📞 Support

- Check logs: `docker-compose logs -f`
- Health check: `curl -k https://yourdomain.com/health`
- Verify DNS: `nslookup yourdomain.com`
- Test connectivity: `curl -v https://yourdomain.com`

---

**Deployment successful! 🎉**

Your application is now running at: `https://yourdomain.com`
