pipeline {
    agent any

    stages {
        stage('Preparation') {
            steps {
                sh '''
					python3 -m venv $VENV_DIR
					. $VENV_DIR/bin/activate
					pip install --upgrade pip
					pip install -r requirements.txt
				'''
            }
        }

        stage('Scraping') {
            steps {
                script {
                    sh 'python3 scraper.py'
                }
            }
        }

        stage('Conversion') {
            steps {
                script {
                    sh 'python3 html_generator.py'
                }
            }
        }
    }
}	
