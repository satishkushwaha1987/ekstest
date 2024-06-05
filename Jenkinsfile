pipeline {
    agent any
    environment {
        dockerimagename = "thetips4you/nodeapp"
        dockerImage = ""
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
    }
}