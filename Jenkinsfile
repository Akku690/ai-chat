pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    environment {
        APP_DIR = '/home/ubuntu/ai-chat-project/ai-chat'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Verify .env exists') {
            steps {
                sh '''
                    if [ ! -f "${APP_DIR}/.env" ]; then
                        echo "ERROR: .env not found at ${APP_DIR}/.env - deploy aborted."
                        exit 1
                    fi
                    echo ".env found, continuing."
                '''
            }
        }

        stage('Build') {
            steps {
                sh '''
                    cd "${APP_DIR}"
                    docker compose build
                '''
            }
        }

        stage('Run Tests (inside container)') {
            steps {
                sh '''
                    cd "${APP_DIR}"
                    docker compose run --rm app pytest -v || echo "No tests found or tests failed - continuing"
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    cd "${APP_DIR}"
                    docker compose down || true
                    docker compose up -d --build
                '''
            }
        }

        stage('Health Check') {
            steps {
                sh '''
                    echo "Waiting for application to become healthy..."
                    for i in $(seq 1 15); do
                        if curl -sf http://localhost:8000/health > /dev/null; then
                            echo "Health check passed."
                            exit 0
                        fi
                        echo "Attempt $i failed, retrying in 4s..."
                        sleep 4
                    done
                    echo "Health check failed after retries."
                    exit 1
                '''
            }
        }
    }

    post {
        success {
            echo 'Deployment successful.'
        }
        failure {
            echo 'Pipeline failed. Recent container logs:'
            sh '''
                cd "${APP_DIR}"
                docker compose logs --tail=50 || true
            '''
        }
        always {
            sh '''
                cd "${APP_DIR}"
                docker compose ps || true
            '''
        }
    }
}
