# Kubernetes Container Orchestration Project Guide

This guide provides step-by-step instructions for completing all Kubernetes orchestration tasks for the Django Messaging App.

## Prerequisites

Ensure you have the following installed:
- Docker
- Minikube
- kubectl
- wrk (for load testing)

### Installation Commands

```bash
# Install Minikube (Linux)
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Install wrk
sudo apt-get install wrk
```

## Project Setup

1. **Build your Docker image first:**
```bash
cd ~/alx-backend-python/messaging_app
docker build -t django-messaging-app:1.0 .
docker build -t django-messaging-app:1.5 .
docker build -t django-messaging-app:2.0 .
```

2. **Copy all Kubernetes files to your project directory:**
```bash
# Ensure all files are in ~/alx-backend-python/messaging_app/
```

## Task 0: Install Kubernetes and Set Up Local Cluster

**Objective:** Start a Kubernetes cluster and verify it's running.

```bash
chmod +x kurbeScript
./kurbeScript
```

**Expected Output:**
- Minikube cluster starts successfully
- Cluster info is displayed
- List of all pods shown

**Verification:**
```bash
kubectl cluster-info
kubectl get nodes
```

## Task 1: Deploy Django App on Kubernetes

**Objective:** Deploy your containerized Django app using Kubernetes.

```bash
kubectl apply -f deployment.yaml
```

**Verification:**
```bash
# Check deployment
kubectl get deployments

# Check pods
kubectl get pods

# Check logs
kubectl logs <pod-name>

# Check service
kubectl get services
```

**Test the deployment:**
```bash
kubectl port-forward service/django-messaging-service 8080:80
curl http://localhost:8080/api/
```

## Task 2: Scale the Django App

**Objective:** Scale the application and perform load testing.

```bash
chmod +x kubctl-0x01
./kubctl-0x01
```

**What this script does:**
1. Scales deployment to 3 replicas
2. Verifies all pods are running
3. Performs load testing with wrk
4. Monitors resource usage

**Manual verification:**
```bash
kubectl get pods -l app=django-messaging
kubectl top pods -l app=django-messaging
```

## Task 3: Set Up Kubernetes Ingress

**Objective:** Expose your Django app externally using Nginx Ingress.

**Follow commands in commands.txt:**

```bash
# Enable Ingress in Minikube
minikube addons enable ingress

# Apply Ingress configuration
kubectl apply -f ingress.yaml

# Verify Ingress
kubectl get ingress
kubectl describe ingress django-messaging-ingress

# Get Minikube IP
minikube ip

# Add to /etc/hosts (replace <MINIKUBE_IP> with actual IP)
echo "<MINIKUBE_IP> django-messaging.local" | sudo tee -a /etc/hosts

# Test access
curl http://django-messaging.local/api/
```

## Task 4: Blue-Green Deployment

**Objective:** Implement zero-downtime deployment using blue-green strategy.

```bash
chmod +x kubctl-0x02
./kubctl-0x02
```

**What this script does:**
1. Deploys blue version (stable)
2. Creates services for both versions
3. Deploys green version (new)
4. Validates both deployments
5. Provides commands to switch traffic

**To switch traffic to GREEN:**
```bash
kubectl patch service django-messaging-service -p '{"spec":{"selector":{"app":"django-messaging","version":"green"}}}'
```

**To switch back to BLUE:**
```bash
kubectl patch service django-messaging-service -p '{"spec":{"selector":{"app":"django-messaging","version":"blue"}}}'
```

**Verification:**
```bash
kubectl get deployments -l app=django-messaging
kubectl get pods -l app=django-messaging
kubectl describe service django-messaging-service
```

## Task 5: Rolling Updates

**Objective:** Update the application without downtime using rolling updates.

The blue_deployment.yaml has been updated to use version 2.0.

```bash
chmod +x kubctl-0x03
./kubctl-0x03
```

**What this script does:**
1. Shows current deployment status
2. Applies updated deployment (v2.0)
3. Monitors rollout progress
4. Tests for downtime with continuous requests
5. Displays success rate and metrics

**Manual rollback (if needed):**
```bash
kubectl rollout undo deployment/django-messaging-blue
kubectl rollout status deployment/django-messaging-blue
```

**View rollout history:**
```bash
kubectl rollout history deployment/django-messaging-blue
```

## Useful Kubernetes Commands

### Pod Management
```bash
# List all pods
kubectl get pods

# Describe a pod
kubectl describe pod <pod-name>

# View logs
kubectl logs <pod-name>

# Execute command in pod
kubectl exec -it <pod-name> -- /bin/bash
```

### Deployment Management
```bash
# List deployments
kubectl get deployments

# Scale deployment
kubectl scale deployment/<name> --replicas=5

# Update image
kubectl set image deployment/<name> <container>=<image>

# Check rollout status
kubectl rollout status deployment/<name>

# Rollback deployment
kubectl rollout undo deployment/<name>
```

### Service Management
```bash
# List services
kubectl get services

# Describe service
kubectl describe service <service-name>

# Port forward
kubectl port-forward service/<service-name> 8080:80
```

### Debugging
```bash
# Get cluster info
kubectl cluster-info

# Get events
kubectl get events

# Get resource usage
kubectl top nodes
kubectl top pods

# Describe resource
kubectl describe <resource-type> <resource-name>
```

## Clean Up

To clean up all resources:

```bash
# Delete deployments
kubectl delete deployment django-messaging-app
kubectl delete deployment django-messaging-blue
kubectl delete deployment django-messaging-green

# Delete services
kubectl delete service django-messaging-service
kubectl delete service django-messaging-service-blue
kubectl delete service django-messaging-service-green

# Delete ingress
kubectl delete ingress django-messaging-ingress

# Stop Minikube
minikube stop

# Delete Minikube cluster
minikube delete
```

## Troubleshooting

### Pods not starting
```bash
kubectl describe pod <pod-name>
kubectl logs <pod-name>
```

### Image pull errors
```bash
# Load image into Minikube
minikube image load django-messaging-app:1.0
minikube image load django-messaging-app:1.5
minikube image load django-messaging-app:2.0
```

### Service not accessible
```bash
kubectl get endpoints
kubectl describe service <service-name>
```

### Ingress not working
```bash
kubectl get pods -n ingress-nginx
kubectl logs -n ingress-nginx <ingress-controller-pod>
```

## Best Practices Demonstrated

1. **Declarative Configurations:** All resources defined in YAML files
2. **Health Checks:** Liveness and readiness probes configured
3. **Resource Limits:** CPU and memory limits set for all containers
4. **Labels and Selectors:** Organized with meaningful labels
5. **Zero Downtime:** Blue-green and rolling update strategies
6. **Monitoring:** Resource monitoring and logging enabled
7. **Security:** ClusterIP services for internal communication
8. **Scalability:** Horizontal scaling demonstrated

## Project Structure

```
messaging_app/
├── kurbeScript                  # Task 0: Start cluster
├── deployment.yaml              # Task 1: Initial deployment
├── kubctl-0x01                  # Task 2: Scaling script
├── ingress.yaml                 # Task 3: Ingress config
├── commands.txt                 # Task 3: Ingress commands
├── blue_deployment.yaml         # Task 4 & 5: Blue version
├── green_deployment.yaml        # Task 4: Green version
├── kubeservice.yaml            # Task 4: Service switching
├── kubctl-0x02                  # Task 4: Blue-green script
└── kubctl-0x03                  # Task 5: Rolling update script
```

## Manual QA Checklist

- [ ] Kubernetes cluster starts successfully
- [ ] Django app deploys and runs
- [ ] Application scales to 3 replicas
- [ ] Load testing completes without errors
- [ ] Ingress controller installed and working
- [ ] External access through Ingress works
- [ ] Blue deployment is stable
- [ ] Green deployment is stable
- [ ] Traffic can switch between blue and green
- [ ] Rolling update completes with zero downtime
- [ ] All pods are healthy after updates

## Request Manual QA Review

Once all tasks are complete and verified, request a manual QA review as instructed in the project requirements.

Good luck with your Kubernetes orchestration project!
