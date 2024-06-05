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
        // stage('Docker Push') {
        //     agent any
        //         steps {
        //             withCredentials([usernamePassword(credentialsId: 'dockerpush', passwordVariable: 'dockerHubPassword', usernameVariable: 'dockerHubUser')]) {
        //             sh "docker login -u ${env.dockerHubUser} -p ${env.dockerHubPassword}"
        //             sh 'docker push shanem/spring-petclinic:latest'
        //             }
        //         }
        //     }
        stage('Docker push') {
            steps{
                script {
                    docker.withRegistry('https://registry.hub.docker.com', 'dockerpush') {            
                    // app.push("${BUILD_NUMBER}")
                    sh 'docker push kushwaha1987/nodeapp:latest'            
                    // app.push("latest")        
                    }
                }
            }    
        }   
    }
}