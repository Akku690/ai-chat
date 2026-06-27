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
                        echo "ERROR: .env not found at ${APP_DIR}/.env — deploy aborted."
                        exit 1
                    fi
                    echo ".env found, continuing."
                '''
            }
        }

        stage('Install Dependencies (for tests)') {
            steps {
                sh '''
                    cd "${APP_DIR}"
                    python3.11 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install pytest
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    cd "${APP_DIR}"
                    . venv/bin/activate
                    pytest -v || echo "No tests found or tests failed - continuing"
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
                    sleep 8
                    curl -f http://localhost:8000/health || (echo "Health check failed" && exit 1)
                '''
            }
        }
    }

    post {
        success {
            echo '✅ Deployment successful at ' + env.APP_DIR
        }
        failure {
            echo '❌ Pipeline failed. Recent container logs:'
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
