#!/usr/bin/env bash

docker build -t gcr.io/qa-edc-ew/hackaton:latest .
docker push gcr.io/qa-edc-ew/hackaton:latest
kubectl apply -f ops/kube/create-web-service.yaml
kubectl apply -f ops/kube/create-web-deployment.yaml

PODS=$(kubectl get pods --namespace=edc-catalog | grep hackaton- | awk '{print $1}')
kubectl delete pods $PODS

watch bash -c "kubectl get pods | grep hackaton-"
