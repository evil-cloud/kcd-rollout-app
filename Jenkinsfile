// Pipeline version: v1.1.5
pipeline {
    agent { label 'jenkins-jenkins-agent' }
    environment {
        IMAGE_NAME      = "d4rkghost47/gitops-api"
        REGISTRY        = "https://index.docker.io/v1/"
        SHORT_SHA       = "${GIT_COMMIT[0..7]}"
        TZ              = "America/Guatemala"  
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    checkout scm
                }
            }
        }

        stage('Build Image') {
            steps {
                container('dind') {
                    script {
                        logInfo("BUILD", "Building Docker image...")
                        try {
                            sh '''
			                export DOCKER_BUILDKIT=1
                            docker build -f Dockerfile.pipeline -t ${IMAGE_NAME}:${SHORT_SHA} .
                            '''
                            logSuccess("BUILD", "Build completed.")
                        } catch (Exception e) {
                            logFailure("BUILD", "Docker build failed: ${e.message}")
                            error("Stopping pipeline due to build failure.")
                        }
                    }
                }
            }
        }
    

        stage('Push Image') {
            steps {
                container('dind') {
                    script {
                        withCredentials([string(credentialsId: 'docker-token', variable: 'DOCKER_TOKEN')]) {
                            logInfo("PUSH", "Uploading Docker image...")
                            try {
                                sh '''
                                echo "$DOCKER_TOKEN" | docker login -u "d4rkghost47" --password-stdin > /dev/null 2>&1
                                docker push ${IMAGE_NAME}:${SHORT_SHA}
                                '''
                                logSuccess("PUSH", "Image pushed successfully.")
                            } catch (Exception e) {
                                logFailure("PUSH", "Docker push failed: ${e.message}")
                                error("Stopping pipeline due to push failure.")
                            }
                        }
                    }
                }
            }
        }

    }

    post {
        success {
            logSuccess("PIPELINE", "Pipeline completed successfully.")
        }
        failure {
            logFailure("PIPELINE", "Pipeline failed.")
        }
    }
}

def logInfo(stage, message) {
    echo "[${stage}] [INFO] ${getTimestamp()} - ${message}"
}

def logSuccess(stage, message) {
    echo "[${stage}] [SUCCESS] ${getTimestamp()} - ${message}"
}

def logFailure(stage, message) {
    echo "[${stage}] [FAILURE] ${getTimestamp()} - ${message}"
}

def getTimestamp() {
    return sh(script: "TZ='America/Guatemala' date '+%Y-%m-%d %H:%M:%S'", returnStdout: true).trim()
}

