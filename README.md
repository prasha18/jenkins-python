# Python Django Application – AWS EKS CI/CD & Observability

## Project Overview

This project demonstrates a complete DevOps workflow for deploying a Python/Django application to **Amazon EKS** with:

- Docker containerization
- Amazon ECR image management
- Jenkins CI/CD
- GitHub webhook-based automatic builds
- Amazon EKS deployment
- Kubernetes Services and Deployments
- Nginx reverse proxy
- AWS Application Load Balancer
- Kubernetes monitoring with Prometheus and Grafana
- Node Exporter and kube-state-metrics
- Kubernetes resource monitoring and dashboards

The application is deployed in the Kubernetes namespace:

```text
my-tnttfc
```

---

# Architecture

```text
                         GitHub
                           |
                           | Push
                           v
                    GitHub Webhook
                           |
                           v
                     +-----------+
                     |  Jenkins  |
                     +-----------+
                           |
              +------------+-------------+
              |                          |
              v                          v
        Docker Build                  AWS ECR
              |                          |
              |                    Docker Image
              +------------->            |
                                        v
                              +-------------------+
                              |     Amazon EKS    |
                              |                   |
                              |   python-app      |
                              |       Pod         |
                              |        :3000      |
                              +---------+---------+
                                        |
                                        | ClusterIP
                                        v
                              +-------------------+
                              |  python-service   |
                              |       :80         |
                              +---------+---------+
                                        |
                                        v
                              +-------------------+
                              |    Nginx Pods     |
                              |       :80         |
                              +---------+---------+
                                        |
                                        v
                              +-------------------+
                              |  AWS ALB / Ingress|
                              +---------+---------+
                                        |
                                        v
                                    Internet


Monitoring Architecture

              +-----------------------+
              |     Python App        |
              +-----------+-----------+
                          |
                          | Application / Pod metrics
                          v
                    Prometheus
                          |
                          v
                      Grafana


              Kubernetes / Node Metrics
                          |
          +---------------+---------------+
          |                               |
          v                               v
   kube-state-metrics                Node Exporter
          |                               |
          +---------------+---------------+
                          |
                          v
                     Prometheus
                          |
                          v
                       Grafana
```

---

# Technologies Used

| Category | Technology |
|---|---|
| Application | Python / Django |
| Containerization | Docker |
| Source Control | Git / GitHub |
| CI/CD | Jenkins |
| Container Registry | Amazon ECR |
| Cloud | AWS |
| Kubernetes | Amazon EKS |
| Kubernetes CLI | kubectl |
| Kubernetes Package Manager | Helm |
| Reverse Proxy | Nginx |
| Load Balancer | AWS Application Load Balancer |
| Monitoring | Prometheus |
| Visualization | Grafana |
| Kubernetes Metrics | kube-state-metrics |
| Node Metrics | Node Exporter |
| AWS Region | `ap-south-1` |

---

# AWS Configuration

## AWS Region

```text
ap-south-1
```

## AWS Account

```text
260369602336
```

## EKS Cluster

```text
devops-eks
```

## Kubernetes Namespace

```text
my-tnttfc
```

## ECR Repository

```text
python-eks-demo
```

Full ECR repository:

```text
260369602336.dkr.ecr.ap-south-1.amazonaws.com/python-eks-demo
```

---

# Project Structure

```text
jenkins-python/
│
├── Dockerfile
├── Jenkinsfile
├── requirements.txt
├── manage.py
├── db.sqlite3
│
├── k8s/
│   ├── ...
│
├── tnttfc/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── tech_repo/
├── techforms/
├── tech_website/
├── templates/
├── static/
├── staticfiles/
├── media/
│
└── README.md
```

---

# 1. GitHub Repository

The source code is maintained in GitHub.

Repository:

```text
https://github.com/prasha18/jenkins-python.git
```

Main branch:

```text
master
```

The Jenkins pipeline uses this repository as its SCM source.

---

# 2. Dockerization

The Django application is containerized using Docker.

The Docker image is built during the Jenkins pipeline.

Example:

```bash
docker build -t python-eks-demo:1 .
```

The image is then tagged for Amazon ECR:

```bash
docker tag \
python-eks-demo:1 \
260369602336.dkr.ecr.ap-south-1.amazonaws.com/python-eks-demo:1
```

---

# 3. Amazon ECR

Amazon ECR is used as the Docker image registry.

## Login to ECR

```bash
aws ecr get-login-password \
  --region ap-south-1 | \
docker login \
  --username AWS \
  --password-stdin \
  260369602336.dkr.ecr.ap-south-1.amazonaws.com
```

## Push image

```bash
docker push \
260369602336.dkr.ecr.ap-south-1.amazonaws.com/python-eks-demo:1
```

The Jenkins pipeline automatically creates an image tag using the Jenkins build number.

Example:

```text
python-eks-demo:15
```

and pushes:

```text
260369602336.dkr.ecr.ap-south-1.amazonaws.com/python-eks-demo:15
```

This avoids repeatedly using the same Docker image tag.

---

# 4. Amazon EKS

The application is deployed to Amazon EKS.

Cluster:

```text
devops-eks
```

Region:

```text
ap-south-1
```

To configure kubectl:

```bash
aws eks update-kubeconfig \
  --region ap-south-1 \
  --name devops-eks
```

Verify access:

```bash
kubectl get nodes
```

---

# 5. Kubernetes Namespace

A dedicated namespace is used for the application:

```bash
kubectl create namespace my-tnttfc
```

Check:

```bash
kubectl get namespace
```

---

# 6. Python Application Deployment

The Django application runs inside the `python-app` Deployment.

Deployment:

```text
python-app
```

Container:

```text
python-app
```

Application container port:

```text
3000
```

Check the Deployment:

```bash
kubectl get deployment python-app -n my-tnttfc
```

Check Pods:

```bash
kubectl get pods -n my-tnttfc -l app=python-app -o wide
```

---

# 7. Python Kubernetes Service

The Python application is exposed internally through:

```text
python-service
```

Service type:

```text
ClusterIP
```

Service port:

```text
80
```

The Service forwards traffic to the Python application container.

Check:

```bash
kubectl get svc python-service -n my-tnttfc
```

---

# 8. Nginx Reverse Proxy

Nginx is used as a reverse proxy between the AWS ALB and the Python application.

The Nginx architecture is:

```text
ALB
 |
 v
nginx-service:80
 |
 v
Nginx Pod
 |
 | proxy_pass
 v
python-service:80
 |
 v
Python Pod:3000
```

There are two Nginx replicas:

```text
nginx
2/2
```

Check:

```bash
kubectl get deployment nginx -n my-tnttfc
kubectl get pods -n my-tnttfc -l app=nginx
```

---

# 9. Nginx Configuration

The Nginx configuration is stored in a Kubernetes ConfigMap.

Example configuration:

```nginx
server {
    listen 80;

    location / {
        proxy_pass http://python-service:80;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

This allows Nginx to forward incoming requests to the Python Kubernetes Service.

---

# 10. AWS Application Load Balancer

The application is exposed externally through an AWS Application Load Balancer using Kubernetes Ingress.

Ingress:

```text
python-app-ingress
```

Ingress class:

```text
alb
```

Check:

```bash
kubectl get ingress -n my-tnttfc
```

The traffic flow is:

```text
Internet
   |
   v
AWS ALB
   |
   v
nginx-service
   |
   v
Nginx
   |
   v
python-service
   |
   v
Python/Django
```

---

# 11. Jenkins CI/CD

Jenkins is installed on a separate EC2 instance.

The Jenkins pipeline performs:

```text
Checkout
   |
   v
Docker Build
   |
   v
AWS Authentication
   |
   v
ECR Login
   |
   v
Push Docker Image
   |
   v
Configure EKS Access
   |
   v
Update Kubernetes Deployment
   |
   v
Wait for Rollout
   |
   v
Verify Deployment
```

---

# 12. Jenkins AWS Credentials

Jenkins uses an AWS credential configured with the ID:

```text
aws-jenkins
```

The pipeline uses this credential for:

- AWS authentication
- ECR access
- EKS access

AWS authentication is tested using:

```bash
aws sts get-caller-identity
```

---

# 13. Jenkins Pipeline

The Jenkins pipeline is stored in:

```text
Jenkinsfile
```

The pipeline:

1. Builds the Docker image.
2. Authenticates with AWS.
3. Logs in to ECR.
4. Tags the Docker image.
5. Pushes the image to ECR.
6. Configures the EKS kubeconfig.
7. Updates the Kubernetes Deployment.
8. Waits for the rollout to complete.
9. Verifies the running image and Pods.

The deployment update is performed using:

```bash
kubectl set image deployment/python-app \
  python-app=260369602336.dkr.ecr.ap-south-1.amazonaws.com/python-eks-demo:${BUILD_NUMBER} \
  -n my-tnttfc
```

Then Jenkins waits for:

```bash
kubectl rollout status deployment/python-app \
  -n my-tnttfc
```

---

# 14. GitHub Webhook

GitHub is configured to automatically trigger Jenkins after a push.

Jenkins trigger:

```text
GitHub hook trigger for GITScm polling
```

GitHub webhook endpoint:

```text
/github-webhook/
```

The workflow is:

```text
Developer
   |
   | git push
   v
GitHub
   |
   | Webhook
   v
Jenkins
   |
   v
Jenkins Pipeline
   |
   v
Docker Build
   |
   v
ECR
   |
   v
EKS
```

This provides automatic CI/CD after a Git push.

---

# 15. Jenkins Pipeline from SCM

Jenkins is configured with:

```text
Definition:
Pipeline script from SCM
```

SCM:

```text
Git
```

Repository:

```text
https://github.com/prasha18/jenkins-python.git
```

Branch:

```text
*/master
```

Script path:

```text
Jenkinsfile
```

Declarative Pipeline automatically performs the SCM checkout.

---

# 16. Kubernetes Deployment Verification

After deployment, Jenkins verifies the Deployment:

```bash
kubectl get deployment python-app \
  -n my-tnttfc
```

Pods:

```bash
kubectl get pods \
  -n my-tnttfc \
  -l app=python-app \
  -o wide
```

Current image:

```bash
kubectl get deployment python-app \
  -n my-tnttfc \
  -o jsonpath='{.spec.template.spec.containers[0].image}'
```

This confirms that the new ECR image is running.

---

# 17. Kubernetes Monitoring

For observability, `kube-prometheus-stack` was installed using Helm.

Monitoring namespace:

```text
monitoring
```

Create namespace:

```bash
kubectl create namespace monitoring
```

Add Prometheus Helm repository:

```bash
helm repo add prometheus-community \
  https://prometheus-community.github.io/helm-charts
```

Update Helm repositories:

```bash
helm repo update
```

Install kube-prometheus-stack:

```bash
helm install monitoring \
  prometheus-community/kube-prometheus-stack \
  --namespace monitoring
```

---

# 18. Monitoring Components

The monitoring stack provides:

### Prometheus

Collects and stores metrics.

### Grafana

Provides dashboards and visualization.

### Alertmanager

Handles alerting.

### Node Exporter

Collects Linux node-level metrics.

### kube-state-metrics

Exposes Kubernetes object/state metrics.

### Prometheus Operator

Manages Prometheus-related Kubernetes resources.

---

# 19. Verify Monitoring

Check Helm:

```bash
helm list -n monitoring
```

Check Pods:

```bash
kubectl get pods -n monitoring
```

Check Services:

```bash
kubectl get svc -n monitoring
```

Expected components include:

```text
alertmanager
grafana
kube-prometheus-operator
kube-state-metrics
prometheus
node-exporter
```

---

# 20. Grafana Access

Grafana is exposed locally using port forwarding:

```bash
kubectl port-forward \
  svc/monitoring-grafana \
  3000:80 \
  -n monitoring
```

Then open:

```text
http://localhost:3000
```

Grafana can also be accessed through the Kubernetes management EC2 host when port forwarding is configured appropriately.

---

# 21. Grafana Dashboards

The kube-prometheus-stack installation provides Kubernetes dashboards.

Examples include:

```text
Kubernetes / Compute Resources / Namespace (Pods)
Kubernetes / Compute Resources / Node (Pods)
Kubernetes / Compute Resources / Nodes Overview
Kubernetes / Compute Resources / Pod
Kubernetes / Compute Resources / Workload
Kubernetes / Controller Manager
Kubernetes / Kubelet
Kubernetes / Networking / Cluster
Kubernetes / Networking / Namespace (Pods)
Kubernetes / Networking / Namespace (Workload)
```

These dashboards can be used to monitor:

- CPU utilization
- Memory utilization
- Pod resource usage
- Node resource usage
- Kubernetes workloads
- Network information
- Cluster resources

---

# 22. Monitoring Architecture

The monitoring stack observes the Kubernetes environment using multiple metric sources.

```text
                    +----------------+
                    |    Grafana     |
                    +-------+--------+
                            |
                            v
                    +----------------+
                    |   Prometheus    |
                    +-------+--------+
                            |
             +--------------+--------------+
             |              |              |
             v              v              v
       Node Exporter   kube-state-      Application
                         metrics          Metrics
             |              |              |
             v              v              v
          EC2 Nodes    Kubernetes       Python App
                       Resources
```

---

# 23. Kubernetes Resource Monitoring

Kubernetes resources can be checked using:

```bash
kubectl get pods -n my-tnttfc
```

```bash
kubectl get deployments -n my-tnttfc
```

```bash
kubectl get services -n my-tnttfc
```

```bash
kubectl get ingress -n my-tnttfc
```

For resource usage:

```bash
kubectl top pods -n my-tnttfc
```

```bash
kubectl top nodes
```

These commands are useful for troubleshooting application performance and resource consumption.

---

# 24. Useful Kubernetes Commands

## View all resources

```bash
kubectl get all -n my-tnttfc
```

## View Pods

```bash
kubectl get pods -n my-tnttfc -o wide
```

## View Deployments

```bash
kubectl get deployments -n my-tnttfc
```

## View Services

```bash
kubectl get svc -n my-tnttfc
```

## View Ingress

```bash
kubectl get ingress -n my-tnttfc
```

## Describe a Pod

```bash
kubectl describe pod <pod-name> -n my-tnttfc
```

## View application logs

```bash
kubectl logs deployment/python-app -n my-tnttfc
```

## Follow logs

```bash
kubectl logs -f deployment/python-app -n my-tnttfc
```

## Restart deployment

```bash
kubectl rollout restart deployment/python-app \
  -n my-tnttfc
```

## Check rollout

```bash
kubectl rollout status deployment/python-app \
  -n my-tnttfc
```

## View rollout history

```bash
kubectl rollout history deployment/python-app \
  -n my-tnttfc
```

## Roll back

```bash
kubectl rollout undo deployment/python-app \
  -n my-tnttfc
```

---

# 25. Useful Jenkins Troubleshooting

Check Jenkins service:

```bash
sudo systemctl status jenkins
```

Check disk usage:

```bash
df -h
```

Check Docker disk usage:

```bash
docker system df
```

Check Docker information:

```bash
docker info
```

Clean unused Docker resources when required:

```bash
docker system prune
```

> Run cleanup commands carefully because unused Docker images, containers and build cache may be removed.

---

# 26. CI/CD Deployment Flow

A complete deployment works as follows:

```text
1. Developer changes Django application
             |
             v
2. git add / git commit
             |
             v
3. git push origin master
             |
             v
4. GitHub receives push
             |
             v
5. GitHub sends webhook to Jenkins
             |
             v
6. Jenkins starts pipeline
             |
             v
7. Jenkins checks out source
             |
             v
8. Docker image is built
             |
             v
9. Jenkins authenticates with AWS
             |
             v
10. Jenkins logs in to ECR
             |
             v
11. Docker image is tagged
             |
             v
12. Image is pushed to ECR
             |
             v
13. Jenkins configures EKS access
             |
             v
14. kubectl set image
             |
             v
15. Kubernetes performs rolling update
             |
             v
16. Jenkins waits for rollout
             |
             v
17. New Python Pod becomes Ready
             |
             v
18. Application is served through
    Python Service -> Nginx -> ALB
```

---

# 27. Final Application Traffic Flow

The final request path is:

```text
Client
  |
  v
AWS Application Load Balancer
  |
  v
python-app-ingress
  |
  v
nginx-service
  |
  v
Nginx Pod
  |
  v
python-service
  |
  v
Python/Django Pod
  |
  v
Application
```

---

# 28. Final Monitoring Flow

Monitoring works independently from the application traffic path:

```text
Python / Kubernetes
        |
        v
   Metric Sources
        |
        v
    Prometheus
        |
        v
     Grafana
        |
        v
 Kubernetes Dashboards
```

---

# 29. Verification Checklist

Use this checklist to verify the complete environment.

## GitHub

```text
[✓] Repository created
[✓] master branch used
[✓] Jenkinsfile committed
[✓] GitHub webhook configured
```

## Docker

```text
[✓] Application containerized
[✓] Docker image builds successfully
```

## ECR

```text
[✓] ECR repository created
[✓] Jenkins authenticates with ECR
[✓] Docker image pushed successfully
[✓] Jenkins build-number image tags used
```

## Jenkins

```text
[✓] Jenkins installed
[✓] AWS credentials configured
[✓] Pipeline configured from SCM
[✓] Docker build working
[✓] ECR push working
[✓] EKS authentication working
[✓] Kubernetes deployment working
[✓] Rollout verification working
```

## GitHub → Jenkins

```text
[✓] GitHub webhook configured
[✓] Push-triggered Jenkins workflow configured
```

## Kubernetes

```text
[✓] EKS cluster running
[✓] Application namespace created
[✓] Python Deployment running
[✓] Python Service running
[✓] Nginx Deployment running
[✓] Nginx Service running
[✓] ALB Ingress configured
```

## Monitoring

```text
[✓] Prometheus installed
[✓] Grafana installed
[✓] Alertmanager installed
[✓] Node Exporter installed
[✓] kube-state-metrics installed
[✓] Kubernetes dashboards available
[✓] Grafana accessible
```
# 30. Key DevOps Concepts Demonstrated

This project demonstrates practical experience with:

- Git workflow
- GitHub
- Docker
- Amazon ECR
- Jenkins
- Jenkins Pipeline
- CI/CD automation
- GitHub Webhooks
- AWS IAM credentials in Jenkins
- Amazon EKS
- Kubernetes Deployments
- Kubernetes Services
- Kubernetes Namespaces
- Kubernetes Ingress
- AWS Application Load Balancer
- Nginx reverse proxy
- Rolling deployments
- Docker image versioning
- Kubernetes rollout verification
- Prometheus
- Grafana
- Alertmanager
- Node Exporter
- kube-state-metrics
- Kubernetes observability

---

# 31. Conclusion

The project implements an end-to-end DevOps deployment pipeline for a Python/Django application.

The completed architecture provides:

```text
GitHub
   |
   v
Jenkins CI/CD
   |
   v
Docker
   |
   v
Amazon ECR
   |
   v
Amazon EKS
   |
   +---- Python Application
   |
   +---- Nginx Reverse Proxy
   |
   +---- AWS ALB
   |
   v
Application Users

The system supports automated application deployment through Jenkins and provides Kubernetes infrastructure monitoring through Prometheus and Grafana.
