pipeline {
    agent any

    tools {
        nodejs 'NodeJS'   // must match name you set in Global Tools
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main',
                    credentialsId: 'github-credentials',
                    url: 'https://github.com/Akku690/ai-chat.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'npm install'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'npm test'
            }
        }

        stage('Build') {
            steps {
                sh 'npm run build'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying application...'
                // Add your deploy command here
                sh 'pm2 restart app || pm2 start app.js --name app'
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline completed successfully!'
        }
        failure {
            echo '❌ Pipeline failed. Check logs above.'
        }
    }
}
