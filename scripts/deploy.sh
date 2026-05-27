#!/bin/bash

# Deploy script
set -e

DEPLOY_HOST=${1:-}
DEPLOY_USER=${2:-}
DEPLOY_PATH=${3:-/opt/smart-chat-ai}

if [ -z "$DEPLOY_HOST" ] || [ -z "$DEPLOY_USER" ]; then
    echo "Usage: ./scripts/deploy.sh <host> <user> [path]"
    exit 1
fi

echo "Deploying to $DEPLOY_USER@$DEPLOY_HOST..."

# Copy files to server
echo "Uploading files..."
scp -r . $DEPLOY_USER@$DEPLOY_HOST:$DEPLOY_PATH

# Run setup on server
echo "Running setup on server..."
ssh $DEPLOY_USER@$DEPLOY_HOST << EOF
    cd $DEPLOY_PATH
    bash scripts/setup.sh
    echo "Deployment complete!"
EOF

echo "✓ Deployment successful"
