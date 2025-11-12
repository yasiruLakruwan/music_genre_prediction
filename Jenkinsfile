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
                    cd AWS_storing       
                    python -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    '''
                }
            }
        }

        stage('Install and build front end'){
            steps{
                script{
                    echo 'Install and build front end.......'
                    sh'''
                    cd frontend
                    node -v
                    npm -v

                    npm install
                    npm run build
                    '''
                }
            }
        }

        stage('Run docker compose (test only)'){
            steps{
                script{
                    echo 'Run docker compose locally(test only).......'
                    sh'''
                    docker-compose up -d
                    docker ps
                    sleep 10
                    docker logs music-backend
                    docker logs music-frontend
                    docker-compose down
                    '''
                }
            }
        }
    }
}


