node {
  git url: 'https://github.com/buildit/jenkins-pipeline-examples.git'
  def mvnHome = tool 'M3'
  sh "${mvnHome}/bin/mvn -B verify"
}
	