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
    }
}