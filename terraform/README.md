# Cloud Functions + Cloud Scheduler

- The resources are in 2 files, gke.tf and cloudsql.tf files just to separate them to be easier to navigate.
- We are assuming that `Terraform Cloud` is being used to create the resources.
- The project variable should be set in `Terraform Cloud`.
- A GCS bucket should already exist.
- The `zip` files `set_node_pool_size.zip` and `turn_on_off.zip`should already exist in a GCS Bucket and the Cloud Function service account must have `permissions` to access the target bucket.
- The timezone being considered is: `America/Sao_Paulo`.
- Each Cloud Function uses the same code depending on the purpose, for example Cloud SQL turn on and turn off are using the same code, the only difference are the variables inside the code which are `OS envs` and are pulled from the Cloud Function `environment` so they should be set using Terraform.
- For CloudSQL the only difference is the `DESIRED_POLICY` variable. When `DESIRED_POLICY` value is `ALWAYS` , then `Cloud SQL is ON` and if `DESIRED_POLICY` value is `NEVER` then `Cloud SQL is OFF`.
- For GKE the only difference is the `DESIRED_NODE_COUNT` variable. When `DESIRED_NODE_COUNT` value is `0` , then `Node Pool` size is 0 and if `DESIRED_NODE_COUNT` value is `3` then `Node Pool` size is 3.

## References

[Cloud SQL Admin API](https://developers.google.com/resources/api-libraries/documentation/sqladmin/v1beta4/python/latest/)

[NodePoolSize docs](https://developers.google.com/resources/api-libraries/documentation/container/v1/python/latest/container_v1.projects.locations.clusters.html)

[Kubernetes API](https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1/projects.locations.clusters.nodePools/setSize)