# Instalation of tools on k8s cluster

## Argo CD
Use helm and follow the instruction from: https://github.com/argoproj/argo-helm

- In case you do not have helm installed yet follow the instruction: https://helm.sh/docs/intro/install/

## Minio DB
Install each file from directory `MinIO-k8s` with kubectl apply command. Example:
- for file `minio-api-svc.yaml` run:
    ```shell
    kubectl apply -f minio-api-svc.yaml
    ```