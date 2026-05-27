# Smart Chat API - CI/CD Configuration

## Environment Setup

The `.env` file should contain:
- `DEBUG`: Set to False in production
- `SECRET_KEY`: Generate with `openssl rand -hex 32`
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `OPENAI_API_KEY`: Your OpenAI API key

## Local Testing Before Deploy

```bash
# 1. Build Docker image
docker-compose build

# 2. Start services
docker-compose up -d

# 3. Run tests
docker-compose exec app pytest

# 4. Test endpoints
curl http://localhost:8000/health
curl http://localhost:8000/docs

# 5. Clean up
docker-compose down
```

## GitHub Actions Setup

### Required Secrets

Set these in GitHub repository settings:

| Secret | Description |
|--------|-------------|
| `DEPLOY_KEY` | SSH private key for deployment |
| `DEPLOY_HOST` | Production server hostname |
| `DEPLOY_USER` | SSH username on server |
| `DEPLOY_PATH` | Deployment directory (/opt/smart-chat-ai) |

### Generate SSH Key

```bash
ssh-keygen -t rsa -b 4096 -f deploy_key -N ""
# Copy deploy_key content to DEPLOY_KEY secret
# Copy deploy_key.pub content to server ~/.ssh/authorized_keys
```

## Build Triggers

The CI/CD pipeline runs on:
- Push to `main` branch
- Push to `develop` branch
- Pull requests to `main` or `develop`

## Pipeline Steps

1. **Build**: Builds Docker image with version tags
2. **Test**: Runs pytest with coverage
3. **Push**: Pushes image to GitHub Container Registry
4. **Deploy** (main branch only): Deploys to production server

## Monitoring Deployment

```bash
# Check workflow status
git push origin main
# View at: https://github.com/yourusername/repo/actions

# Monitor server after deploy
ssh user@host
cd /opt/smart-chat-ai
docker-compose logs -f app
```

## Rollback

If deployment fails:

```bash
# On server
cd /opt/smart-chat-ai

# View previous image tags
docker images | grep smart-chat-ai

# Rollback to previous version
docker-compose pull  # (specify tag in docker-compose.yml)
docker-compose up -d

# Verify health
curl https://yourdomain.com/health
```

## Troubleshooting

### Deployment fails at health check
- SSH to server and check logs: `docker-compose logs app`
- Ensure .env file exists and has correct values
- Check port 443 is accessible: `curl -k https://localhost/health`

### Tests fail in GitHub Actions
- Check test output in GitHub Actions UI
- Run locally: `docker-compose exec app pytest -v`
- Look for missing dependencies in requirements.txt

### Image not pushing to registry
- Verify GitHub token has push permission
- Check container registry authentication

See DEPLOYMENT.md for detailed troubleshooting.
