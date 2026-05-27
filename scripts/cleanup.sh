#!/bin/bash

# Cleanup script for development
set -e

echo "Cleaning up Smart Chat AI project..."

echo "Stopping Docker containers..."
docker-compose down

echo "Removing volumes (WARNING: This will delete all data)..."
read -p "Are you sure? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    docker-compose down -v
    echo "✓ Volumes removed"
fi

echo "Removing build artifacts..."
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete

echo "✓ Cleanup complete"
