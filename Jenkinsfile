pipeline{
    agent any

    stages{
        stage('Cloning github repo to jenkins'){
            steps{
                script{
                    echo 'Cloning github repo to jenkins.....'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-music', url: 'https://github.com/yasiruLakruwan/music_genre_prediction.git']])
                }
            }
        }

        stage('Setting up virtual environment and dependancies'){
            steps{
                script{
                    echo 'Setting up virtual environment and dependancies....'
                    sh'''
                    # Move to backend folder
                    cd AWS_storing
                    # create a python environment
                    python -m venv venv
                    # Activate it
                    . venv/bin/activate
                    # Upgrade pip
                    pip install --upgrade pip
                    # Install project dependancies
                    pip install -r requirements.txt
                    
                    '''
                }
            }
        }
    }

}