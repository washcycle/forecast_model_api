#!/bin/sh
# ~/start-minikube.sh
if ! minikube status -p forecast-model-cluster | grep -q "Running"; then
    minikube start -p forecast-model-cluster
fi
