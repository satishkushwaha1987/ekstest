pipeline {
    agent any
    environment {
        dockerimagename = "kushwaha1987/nodeapp"
        dockerImage = "docker"
        APP_NAME = "eksapp"
    }
    stages {
        stage ('git checkout') {
            steps {
                git 'https://github.com/shazforiot/nodeapp_test.git'
            }   
        }
        stage('Build Image') {
            steps {
                script {
                    dockerImage = docker.build dockerimagename
                }
            }
        }
        stage ('docker push') {
            environment {
                registryCredential = 'dockerpush'
            }
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', registryCredential) {
                        dockerImage.push("latest")
                    }
                }
            }
        }
        stage('Deploying app to k8s') {
            steps {
                sh 'kubectl apply -f deploymentservice.yml'
            }
        }
    }
}    

       
