pipeline {
    agent any
    environment {
        dockerimagename = "kushwaha1987/nodeapp"
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
        stage('docker push') {
            steps{
                script {
                    docker.withRegistry('https://registry.hub.docker.com', 'dockerpush') {            
                    // app.push("${BUILD_NUMBER}")
                    //sh 'docker tag kushwaha1987/nodeapp kushwaha1987/nodeapp'
                    sh 'docker push kushwaha1987/nodeapp'          
                    // app.push("latest")        
                    }
               }
            }
        }
    }    
}
       
