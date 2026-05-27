version: 1

dirs:
  - path: app
    files:
      - main.py
      - config.py
      - database.py
      - schemas.py
      - security.py
      - __init__.py
  - path: app/models
    files:
      - __init__.py
      - user.py
      - conversation.py
      - message.py
      - analytics.py
  - path: app/routes
    files:
      - __init__.py
      - auth.py
      - conversations.py
      - analytics.py
      - health.py
  - path: app/services
    files:
      - __init__.py
      - cache.py
      - ai.py
      - database.py
  - path: nginx
    files:
      - nginx.conf
  - path: scripts
    files:
      - init-db.sql
      - setup.sh
      - cleanup.sh
      - deploy.sh
  - path: .github/workflows
    files:
      - build-deploy.yml

root_files:
  - Dockerfile
  - docker-compose.yml
  - requirements.txt
  - .env.example
  - .dockerignore
  - README.md
  - SECURITY.md
  - DEPLOYMENT.md
  - DEVELOPMENT.md
