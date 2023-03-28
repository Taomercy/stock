node('docker-build') {
    ws("/root/stock-pipeline"){
        stage('Clone') {
            sh "rm -rf stock"
            sh "git clone https://gitlab.com/Taomercy/stock.git"
            script {
                build_tag = sh(returnStdout: true, script: 'cd stock;git rev-parse --short HEAD').trim()
                println "build_tag: ${build_tag}"
            }
        }
        ws("stock"){
            stage('Build') {
                sh "docker build -t taomercy/stock-monitor:${build_tag} ."
            }

            stage('Push') {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-wuwei', passwordVariable: 'dockerHubPassword', usernameVariable: 'dockerHubUser')]) {
                    sh "docker login -u ${dockerHubUser} -p ${dockerHubPassword}"
                    sh "docker push taomercy/stock-monitor:${build_tag}"
                }
            }

            stage('Remove old container'){
                sh "docker ps -a | grep stock-monitor | awk {'print \$1'} | xargs docker stop"
                sh "docker ps -a | grep stock-monitor | awk {'print \$1'} | xargs docker rm"
            }

            stage('Start new container') {
                sh "docker run -id --name=stock-monitor taomercy/stock-monitor:${build_tag}"
            }
        }
    }
}
