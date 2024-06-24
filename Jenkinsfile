pipeline {
    agent any
    environment {
        dockerimagename = "kushwaha1987/pythonapp"
        dockerImage = "docker"
    //     APP_NAME = "eksapp"
    }
    stages {
    //     stage ('git checkout') {
    //         steps {
    //             script{
	// 		         git branch: 'logs', url: "https://github.com/zestdent/zestmobileoptimization.git"
	// 		    }
    //         }   
    //     }
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
                sh 'kubectl apply -f mariadb-pvc.yaml --validate=false'
                sh 'kubectl apply -f mariadb-statefulset.yaml --validate=false'
                sh 'kubectl apply -f app-deployment.yaml --validate=false'
            }
        }
    }
}    

       
