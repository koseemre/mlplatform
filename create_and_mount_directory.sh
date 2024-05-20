# Description: Create and mount directories for minikube
mkdir $HOME/data
mkdir $HOME/data/model-files
mkdir $HOME/data/mongo-data
mkdir $HOME/data/grafana-data
mkdir $HOME/data/logs
mkdir $HOME/data/prometheus-data

minikube mount $HOME/data:/data