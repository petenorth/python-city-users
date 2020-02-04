pipeline{
  stages{
    stage ('checkout'){
      steps{
        checkout scm
      }
    }
    stage ('install modules'){
      steps{
        sh '''
          docker build -f Dockerfile -t python-city-users:latest .
        '''
      }
    }
  }
}
