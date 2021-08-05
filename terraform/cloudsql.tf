module "cloudsql-function-turn-off"{
  source                  = "github.com/brunog-caylent/gcp-terraform/tree/main/modules/cloudfunctions"
  project                 = var.project
  cloud_function_name     = "cloudsql-function-turn-off"
  function_runtime        = "python37"
  description             = "Cloud function to automate the stop of a Cloud SQL instance"
  available_memory_mb     = 256
  trigger_http            = true
  entry_point             = "cloudsql"
  ingress_settings        = "ALLOW_ALL"
  svc_acc_prefix          = "svc-terraform"
  source_archive_bucket   = "test-bucket"
  source_archive_object   = "bucket-name/folder1/folder2/turn_on_off.zip"

  env_variables           = {
    DESIRED_POLICY        = "NEVER"
    INSTANCE_NAME         = "test-instance"
  }

}

module "cloudsql-turn-off-job" {
  source                  = "github.com/brunog-caylent/gcp-terraform/tree/main/modules/cloudscheduler"
  project                 = var.project
  job_name                = "cloudsql-turn-off-job"
  description             = "Job responsible for triggering a Cloud Function that stops a Cloud SQL instance, it should be scheduled to run at 7pm everyday(after business hours)"
  cron_schedule           = "0 19 * * 1-5" # At 19:00 on every day-of-week from Monday through Friday.
  min_backoff_duration    = "2s"
  max_backoff_duration    = "10s"
  cloud_function_uri      = module.cloudsql-function-turn-off.url
  svc_account             = module.cloudsql-function-turn-off.svc_account
}