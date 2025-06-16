pipeline {
    agent any
    stages {
        stage('Start') {
            steps {
                echo "Début de l'analyse des logs"
            }
        }
        pipeline {
    agent any
    stages {
        stage('Analyze') {
            steps {
                bat 'python log_analyzer.py .'
                echo " Analyse terminée avec succès"
                script {
                    if (fileExists('rapport.txt')) {
                        echo "Rapport généré avec succès"
                        echo "Contenu du rapport :"
                        echo readFile('rapport.txt')
                        archiveArtifacts artifacts: 'rapport.txt', fingerprint: true, allowEmptyArchive: true
                    } else {
                        echo "Aucun rapport généré"
                        currentBuild.result = 'UNSTABLE'
                    }
                }
                bat 'dir'
            }
        }
    }
}

        stage('End') {
            steps {
                script {
                    if (fileExists('log.txt')) {
                        archiveArtifacts artifacts: 'log.txt', allowEmptyArchive: true
                    }
                }
                echo "Fin du pipeline"
            }
        }
    }
}
