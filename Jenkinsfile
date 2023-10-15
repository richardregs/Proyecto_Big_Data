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
                    def deployScript = './deploy.sh' // Ruta relativa al Jenkinsfile
                    sh "chmod +x ${deployScript}" // Asegúrate de que tenga permisos de ejecución
                    sh "./${deployScript}" // Ejecuta el script
                }
            }
        }
    }
}