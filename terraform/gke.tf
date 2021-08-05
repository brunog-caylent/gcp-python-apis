module "gke-setnodepoolsize-zero"{
  source                  = "github.com/brunog-caylent/gcp-terraform/tree/main/modules/cloudfunctions"
  project                 = var.project
  cloud_function_name     = "gke-setnodepoolsize-zero"
  function_runtime        = "python37"
  description             = "Cloud function to reduce the size of a node pool to 0 in order to save costs"
  available_memory_mb     = 256
  trigger_http            = true
  entry_point             = "set_node_pool_size"
  ingress_settings        = "ALLOW_ALL"
  svc_acc_prefix          = "svc-terraform"
  source_archive_bucket   = "cloud-functions-bucket"
  source_archive_object   = "bucket-name/folder1/folder2/set_node_pool_size.zip"

  env_variables           = {
    CLUSTER_LOCATION      = "us-east1"
    CLUSTER_NAME          = "test-cluster"
    NODE_POOL_NAME        = "test-node-pool"
    DESIRED_NODE_COUNT    = "0"
  }

}

module "gke-setnodepoolsize-zero-job" {
  source                  = "github.com/brunog-caylent/gcp-terraform/tree/main/modules/cloudscheduler"
  project                 = var.project
  job_name                = "gke-setnodepoolsize-zero"
  description             = "Job responsible for triggering a Cloud Function that sets a node pool size to 0 instances at 7pm everyday(end of business hours)"
  cron_schedule           = "0 19 * * 1-5" # At 19:00 on every day-of-week from Monday through Friday.
  min_backoff_duration    = "2s"
  max_backoff_duration    = "10s"
  cloud_function_uri      = module.gke-setnodepoolsize-zero.url
  svc_account             = module.gke-setnodepoolsize-zero.svc_account
}