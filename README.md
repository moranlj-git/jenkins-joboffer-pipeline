Jenkins Job Offer Pipeline

1 Préparation (Install)

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

2 Scraping

 stage('Scraping') {
            steps {
                script {
                    sh 'python3 scraper.py'
                }
            }
        }

3 Transformation HTML

  stage('Conversion') {
        steps {
             script {
                 sh 'python3 html_generator.py'
             }
          }
    }

4 Validation / Tests

        stage('Tests') {
            steps {
                script {
                    def csvLineCount = sh(script: 'wc -l < data/jobs.csv', returnStdout: true).trim().toInteger()
                    def htmlContent = readFile('public/index.html')

                    if (csvLineCount < 10) {
                        echo "ERROR: jobs.csv has less than 10 lines: ${csvLineCount}"
                        currentBuild.result = 'FAILURE'
                        error('jobs.csv line count check failed')
                    }

                    if (!htmlContent.contains('<table>') || (htmlContent.split('<tr>').size() -1) < 10) {
                        echo "ERROR: index.html does not contain <table> or has less than 10 rows"
                        currentBuild.result = 'FAILURE'
                        error('index.html content check failed')
                    }
                }
            }
        }

5 Détection de changements
        stage('DetectChanges') {
            steps {
                script {
                    def jobsCsvExists = fileExists('data/jobs_previous.csv')

                    if (!jobsCsvExists) {
                        echo "No previous jobs.csv found.  Proceeding."
                        sh 'cp data/jobs.csv data/jobs_previous.csv'
                    } else {
                        def md5Current = sh(script: 'md5sum data/jobs.csv | cut -d " " -f 1', returnStdout: true).trim()
                        def md5Previous = sh(script: 'md5sum data/jobs_previous.csv | cut -d " " -f 1', returnStdout: true).trim()

                        if (md5Current == md5Previous) {
                            echo "Aucune nouvelle offre. Terminating pipeline."
                            currentBuild.result = 'SUCCESS'
                            return
                        } else {
                            echo "Changes detected.  Proceeding."
                            sh 'cp data/jobs.csv data/jobs_previous.csv'
                        }
                    }
                }
            }
        }
6 Archivage
        stage('Archive') {
            steps {
                archiveArtifacts artifacts: 'data/jobs.csv, public/index.html, logs/log.txt', allowEmptyArchive: true
            }
        }
7 Déploiement

		stage('Deploy') {
			steps {
				sh '''
					#!/bin/bash
					set -e

					# The absolute path to your Nginx web directory
					DEPLOY_PATH="/var/www/html/"

					# Ensure the destination directory exists
					mkdir -p "$DEPLOY_PATH"

					# Copy the file directly
					cp public/index.html "$DEPLOY_PATH"

					echo "Successfully deployed to $DEPLOY_PATH"
				'''
			}
		}

8 Déclenchement automatique

    triggers {
        // Example: Trigger every 6 hours
        cron('H */6 * * *')
    }
