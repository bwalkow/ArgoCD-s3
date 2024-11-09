# ArgoCD-s3
Description of the integration of ArgoCD with the s3 database

## Problem statement
As the integration of ArgoCD events with the triggers available on s3 has not been described in a way that does not leave significant questions, as I found out during my first approach to this problem, I decided to share my experience, which may make the implementation of this solution easier for other developers.

## Tools
List of tools used in integration:
- [ArgoCD server](https://github.com/argoproj/argo-cd)
- [MinIO s3 database](https://min.io/docs/minio/container/index.html)

## Runtime environment
- kubernetes (installation described in `Kubernetes-installation.md` file)



### Add argo endpoint to MinIO
- Run command:
    ```shell
    export MINIO_ROOT_USER=your_minio_root && export MINIO_ROOT_PASSWORD=your_minio_pass
    ```
    ```shell
    mc alias set myminio http://minio:9000 $MINIO_ROOT_USER $MINIO_ROOT_PASSWORD
    ```
    ```shell
    mc admin config set myminio notify_webhook:1 endpoint="http://argo-endpoint"
    ```

- Or use GUI, go to:
    1. Events 
    2. Event Destinations
    4. Add Webhook Event Destination like in example:
        ```
        ARN: argo-endpoint
        Endpoint: http://argo-endpoint
        Auth Token: your-authorization-token
        ```
    5. Save


### Setup bucket events
Go to:
1. Your bucket name
2. Manage
3. (On the left) Events 
4. Subscribe to Event
5. Select previously added endpoint
    ```
    ARN: argo-endpoint
    prefix: data/dir1/subdir1
    suffix: .extension
    Select Event: PUT
    ```
6. Save
