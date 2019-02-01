node {	
stage('Checkout code') {
        steps {
            checkout scm
        }
    }
	
stage('Testcases) {
		steps{
			robot CJP_Robot_Testing.robot
		}
	}
	