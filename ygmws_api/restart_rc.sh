#!/bin/bash
kubectl delete -f ./rc.yaml
kubectl create -f ./rc.yaml
kubectl get pod