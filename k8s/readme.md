# Kubernetes Setup for BBurger Project

This README provides instructions to set up and manage the BBurger project using Kubernetes.

## Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Kind (Kubernetes IN Docker)](https://kind.sigs.k8s.io/docs/user/quick-start/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/)

## Setup

### 1. Create a Kubernetes Cluster with Kind

First, ensure Docker is running, then create a cluster using Kind:

~ kind create cluster --name bburger-cluster


### 2. Configure kubectl

Make sure kubectl is configured to use the new cluster:



~ kubectl cluster-info --context kind-bburger-cluster


### 3. Deploy the Application

Navigate to the k8s directory where your Kubernetes configuration files are located and apply the configurations:



~ kubectl apply -f k8s/

This command applies all the configurations in the k8s directory.


###  4. Verify the Deployment

Check the status of your pods to ensure everything is running correctly:


~ kubectl get pods

You should see the pods for your application running. If not, wait for ready 2/2.


### Apply migrations 

kubectl exec -it <POD_NAME> -c app -- python /usr/src/app/manage.py migrate


### Accessing the Application

To access the Django application, you need to forward the port from the Kubernetes cluster to your local machine. Use the following command to forward the port:


~ kubectl port-forward svc/django-service 8080:80

You can now access the application in your browser at http://localhost:5000.
Stopping the Cluster


### For logs

~ kubectl logs <pod_name> -c app
~ kubectl logs <pod_name> -c db

To stop the Kind cluster without deleting it, you can stop the Docker containers:

~ docker stop <container_id>

Replace <container_id> with the ID of the Kind container, which you can find using:


~ docker ps


To restart the cluster, use:


~ docker start <container_id>


Deleting the Cluster

If you want to delete the cluster, use the following command:


~kind delete cluster --name bburger-cluster


### Troubleshooting

If needed delete a pod it is replaced 

~ kubectl delete pod <nome-do-pod>


Port Conflict

If you encounter a port conflict (e.g., 5432 is already in use), you can:

    Stop the PostgreSQL service on your local machine:

    sudo systemctl stop postgresql

    Change the port configuration in your docker-compose.yml or Kubernetes service definition.

DisallowedHost Error

If you encounter a DisallowedHost error, add the IP address to your Django ALLOWED_HOSTS setting in the settings.py file:

python

ALLOWED_HOSTS = ['172.18.0.2:30001', 'localhost', '127.0.0.1']

