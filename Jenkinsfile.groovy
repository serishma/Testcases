stage('Publish Robot results') {
    steps {
        script {
          step(
            [
              $class              : 'RobotPublisher',
              outputPath          : 'C:/Users/pserishm/Documents/PHC_Automation/',
              outputFileName      : "C:/Users/pserishm/Documents/PHC_Automation/output.xml",
              reportFileName      : 'C:/Users/pserishm/Documents/PHC_Automation/report.html',
              logFileName         : 'C:/Users/pserishm/Documents/PHC_Automation/log.html',
              disableArchiveOutput: false,
              passThreshold       : 95,
              unstableThreshold   : 90,
              otherFiles          : "**/*.png,**/*.jpg",
            ]
          )
        }
  }
}
stage("Testing") 
		{
		
		}			
		
		