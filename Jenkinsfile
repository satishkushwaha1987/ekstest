pipeline {
    agent any
    environment {
        dockerimagename = "thetips4you/nodeapp"
        dockerImage = ""
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
        stage('Docker push') {
            steps{
                script {
                    docker.withRegistry('https://registry.hub.docker.com', 'dockerpush') {            
                    app.push("${env.BUILD_NUMBER}")            
                    app.push("latest")        
                    }
                }
            }    
        }   
    }
}