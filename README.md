# ArgoCD-s3
Description of the integration of ArgoCD with the s3 database

## Problem statement
As the integration of ArgoCD events with the triggers available on s3 has not been described in a way that does not leave significant questions, as I found out during my first approach to this problem, I decided to share my experience, which may make the implementation of this solution easier for other developers.

## Tools
List of tools used in integration:
- [ArgoCD server](https://github.com/argoproj/argo-cd)
- [MinIO s3 database](https://min.io/docs/minio/container/index.html)

## Runtime environment
- docker (Not described yet)
- kubernetes (installation described in `Kubernetes-installation.md` file)


### Add argo endpoint to MinIO
Go to:
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
2. (On the left) Events 
3. Subscribe to Event
4. Select previously added endpoint
    ```
    ARN: argo-endpoint
    prefix: data/dir1/subdir1
    suffix: .extension
    Select Event: PUT
    ```
5. Save
