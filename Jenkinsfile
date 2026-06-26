pipeline {
    agent any

    stages {
        stage('Install Dependencies') {
            steps {
                dir('app') {
                    sh 'npm install'
                }
            }
        }

        stage('Run Tests') {
            steps {
                dir('app') {
                    sh 'npm test'
                }
            }
        }

        stage('Build') {
            steps {
                dir('app') {
                    sh 'npm run build'
                }
            }
        }

        stage('Deploy') {
            steps {
                dir('app') {
                    echo 'Deploying...'
                    sh 'pm2 restart app || pm2 start app.js --name app'
                }
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
