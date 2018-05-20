k8s部署时的标签列表:
kubectl label nodes 172.18.248.190 ygawcde_api=master
kubectl label nodes 172.18.248.190 ygawcde_driver=master

kubectl label nodes 172.18.248.190 ygawcde_mgmt=master

kubectl label nodes 172.18.248.190 ygawcde_scheduler=master
kubectl label nodes 172.18.248.195 ygawcde_scheduler=master

kubectl label nodes 172.18.248.190 ygawcde_extractor=master
kubectl label nodes 172.18.248.195 ygawcde_extractor=master
