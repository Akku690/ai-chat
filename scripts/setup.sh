#!/bin/bash

# Setup script for local development
set -e

echo "Setting up Smart Chat AI project..."

# Create .env file
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Update .env with your configuration, especially OPENAI_API_KEY"
else
    echo "✓ .env file already exists"
fi

# Create SSL certificates for development
if [ ! -d nginx/ssl ]; then
    echo "Creating self-signed SSL certificates for development..."
    mkdir -p nginx/ssl
    openssl req -x509 -newkey rsa:4096 -keyout nginx/ssl/key.pem -out nginx/ssl/cert.pem \
        -days 365 -nodes -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"
    echo "✓ Self-signed certificates created"
else
    echo "✓ SSL certificates directory exists"
fi

# Build and start services
echo "Building Docker images..."
docker-compose build

echo ""
echo "Starting services..."
docker-compose up -d

echo ""
echo "Waiting for services to be healthy..."
sleep 10

# Check services
echo ""
echo "Service status:"
docker-compose ps

echo ""
echo "✓ Setup complete!"
echo ""
echo "Available endpoints:"
echo "  - API: http://localhost:8000"
echo "  - API Docs: http://localhost:8000/docs"
echo "  - HTTPS: https://localhost (self-signed)"
echo "  - PostgreSQL: localhost:5432"
echo "  - Redis: localhost:6379"
echo ""
echo "Next steps:"
echo "  1. Update .env with your OPENAI_API_KEY"
echo "  2. Run: docker-compose restart app"
echo "  3. Visit http://localhost:8000/docs to test the API"
