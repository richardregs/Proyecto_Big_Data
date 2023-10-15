pipeline{
    agent any
    stages{
        stage ('Build'){
            steps{
                echo "BUILD stage disabled"
            }
        }
        stage ('Tests'){
            steps{
                echo "TEST stage disabled"
            }
        }
        stage ('Coverage'){
            steps{
                echo "Coverage stage disabled"
            }
        }
        stage ('Fortify'){
            steps{
                echo "Fortify stage disabled"
            }
        }
        stage ('Deploy'){
            steps{
                echo "DEPLOY stage disabled"
                script {
                    def deployDirectory = '/var/lib/jenkins/workspace/deploy-mtericas-JOB-api'

                    echo "Ingresando al directorio de despliegue"
                    sh "cd ${deployDirectory}"

                    echo "Ejecutando docker-compose para desplegar la aplicación"
                    sh "sudo docker-compose down"
                    sh "sudo docker-compose up -d"
                }
            }
        }
    }
}