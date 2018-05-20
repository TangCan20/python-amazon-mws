#!/bin/bash

sudo docker rmi -f $SPIDER_REGISTRY:5000/ygawcde_scheduler:latest
sudo docker build -t $SPIDER_REGISTRY:5000/ygawcde_scheduler:latest ./
sudo docker push $SPIDER_REGISTRY:5000/ygawcde_scheduler:latest

kubectl delete -f ./rc.yaml
kubectl create -f ./rc.yaml
kubectl get pod
