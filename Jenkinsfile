// Pipeline version: v1.1.7
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
                    checkout([$class: 'GitSCM', branches: [[name: '*/main']],
                            extensions: [[$class: 'CleanBeforeCheckout']],
                            userRemoteConfigs: [[url: 'https://github.com/evil-cloud/kcd-rollout-app.git']]])
                }
            }
        }

        stage('Build Image') {
            steps {
                container('dind') {
                    script {
                        sh '''
			            export DOCKER_BUILDKIT=1
                        docker build -f Dockerfile.pipeline -t ${IMAGE_NAME}:${SHORT_SHA} .
                        '''
                    }
                }
            }
        }

        stage('Push Image') {
            steps {
                container('dind') {
                    script {
                        withCredentials([string(credentialsId: 'docker-token', variable: 'DOCKER_TOKEN')]) {
                            sh '''
                            echo "$DOCKER_TOKEN" | docker login -u "d4rkghost47" --password-stdin > /dev/null 2>&1
                            docker push ${IMAGE_NAME}:${SHORT_SHA}
                            '''
                        }
                    }
                }
            }
        }
    }
}
