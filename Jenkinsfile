pipeline {
    agent any

    environment {
        AWS_REGION = 'ap-south-1'
        AWS_ACCOUNT_ID = '260369602336'

        ECR_REPOSITORY = 'python-eks-demo'
        ECR_REGISTRY = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"

        EKS_CLUSTER = 'devops-eks'
        K8S_NAMESPACE = 'my-tnttfc'

        DEPLOYMENT_NAME = 'python-app'
        CONTAINER_NAME = 'python-app'
    }

    stages {

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build \
                      -t ${ECR_REPOSITORY}:${BUILD_NUMBER} .
                '''
            }
        }

        stage('Test AWS Authentication') {
            steps {
                withCredentials([
                    [$class: 'AmazonWebServicesCredentialsBinding',
                     credentialsId: 'aws-jenkins']
                ]) {
                    sh '''
                        aws sts get-caller-identity
                    '''
                }
            }
        }

        stage('Login to ECR') {
            steps {
                withCredentials([
                    [$class: 'AmazonWebServicesCredentialsBinding',
                     credentialsId: 'aws-jenkins']
                ]) {
                    sh '''
                        aws ecr get-login-password \
                          --region ${AWS_REGION} | \
                        docker login \
                          --username AWS \
                          --password-stdin ${ECR_REGISTRY}
                    '''
                }
            }
        }

        stage('Push Image to ECR') {
            steps {
                sh '''
                    docker tag \
                      ${ECR_REPOSITORY}:${BUILD_NUMBER} \
                      ${ECR_REGISTRY}/${ECR_REPOSITORY}:${BUILD_NUMBER}

                    docker push \
                      ${ECR_REGISTRY}/${ECR_REPOSITORY}:${BUILD_NUMBER}
                '''
            }
        }

        stage('Configure EKS Access') {
            steps {
                withCredentials([
                    [$class: 'AmazonWebServicesCredentialsBinding',
                     credentialsId: 'aws-jenkins']
                ]) {
                    sh '''
                        export KUBECONFIG="$WORKSPACE/kubeconfig"

                        aws eks update-kubeconfig \
                          --region ${AWS_REGION} \
                          --name ${EKS_CLUSTER} \
                          --kubeconfig "$KUBECONFIG"

                        kubectl get nodes
                    '''
                }
            }
        }

        stage('Deploy to EKS') {
            steps {
                withCredentials([
                    [$class: 'AmazonWebServicesCredentialsBinding',
                     credentialsId: 'aws-jenkins']
                ]) {
                    sh '''
                        export KUBECONFIG="$WORKSPACE/kubeconfig"

                        kubectl set image deployment/${DEPLOYMENT_NAME} \
                          ${CONTAINER_NAME}=${ECR_REGISTRY}/${ECR_REPOSITORY}:${BUILD_NUMBER} \
                          -n ${K8S_NAMESPACE}

                        kubectl rollout status \
                          deployment/${DEPLOYMENT_NAME} \
                          -n ${K8S_NAMESPACE}
                    '''
                }
            }
        }

        stage('Verify Deployment') {
            steps {
                withCredentials([
                    [$class: 'AmazonWebServicesCredentialsBinding',
                     credentialsId: 'aws-jenkins']
                ]) {
                    sh '''
                        export KUBECONFIG="$WORKSPACE/kubeconfig"

                        echo "===== Deployment ====="

                        kubectl get deployment python-app \
                          -n my-tnttfc

                        echo "===== Pods ====="

                        kubectl get pods \
                          -n my-tnttfc \
                          -l app=python-app \
                          -o wide

                        echo "===== Current Image ====="

                        kubectl get deployment python-app \
                          -n my-tnttfc \
                          -o jsonpath='{.spec.template.spec.containers[0].image}'

                        echo
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'Python application deployed successfully.'
        }

        failure {
            echo 'Deployment failed. Check the Jenkins console output.'
        }
    }
}
