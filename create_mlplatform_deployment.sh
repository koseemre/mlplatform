: 'Description: This script creates the deployment for the inference-server and model-registry services in the mlplatform namespace.
The script also creates the deployment for the mongo db deployment with its service'

# create the namespace
echo "Creating the namespace"
kubectl create namespace mlplatform

# create the mongo db service
echo "Creating the mongo db service"
docker-compose -f mongo_docker_compose.yml up -d

# build the images
echo "Building the ml platform images .."
docker build -t model-registry model-registry/.
docker build -t inference-server inference-server/.
echo "Building the ml platform done"

# remove the images from minikube if they already exist
echo "Removing images minikube if they already exist .."
minikube image unload model-registry:latest
minikube image unload inference-server:latest

# load the images into minikube
echo "Loading images into minikube"
minikube image load model-registry:latest
minikube image load inference-server:latest

# delete the deployments if they already exist
echo "Deleting the deployments/services if they already exist"
kubectl delete -f model_registry.yaml
kubectl delete -f inference_server.yaml

# create deployments for the inference-server and model-registry
echo "Creating deployments for the inference-server and model-registry"
kubectl create -f model_registry.yaml
kubectl create -f inference_server.yaml

# create services for the deployments (inference-server and model-registry)
echo "Creating services for the deployments"
kubectl expose deployment model-registry -n mlplatform --type=NodePort --port=8080 --target-port=8080
kubectl expose deployment inference-server -n mlplatform --type=NodePort --port=8080 --target-port=8080

# create the ingress
kubectl apply -f ingresses.yaml

# create prometheus and grafana services
echo "Creating the prometheus and grafana services"
kubectl apply -f ./prometheus-grafana/prometheus_deployment.yml
kubectl apply -f ./prometheus-grafana/grafana_deployment.yml