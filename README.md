# GCP Pyhton APIs

- We will use Cloud Functions that will be usin python to interact with the Google Cloud APIs, in this case, GKE and CloudSQL APIs.


## How to use/interact with it

- The bucket and eventual files can be created with Terraform, files can also be uploaded using gsutil.

  > In this use case we are assuming that files are already uploaded to an existing GCS bucket.

## Using `gsutil` command line to upload the files:

1 - Go to the desired path where the files `main.py and requirements.txt` are;
2 - Select the 2 files and zip them into a new zip file. `Note:` Do not zip the folder where the 2 files are. Cloud Function is not able to read folders. The zip archive must have only 2 files inside it, `main.py and requirements.txt`. It `can't` be a zip file with a folder inside it.
3 - Open the terminal;  
4 - Run the following commands:  

```
gcloud config set project <project_name>

gsutil cp < path on your computer with the zip archive(.zip) > gs://<bucket_name>/folder_if_you__want/<other_folder_if_you__want>/<api_name>/
```

> At this point you should already be able to see the files in the desired location inside the GCS bucket.

5 - Deploy the Cloud function via Terraform pointing to the path in the bucket.
6 - Optional: You can create Cloud Scheduler job to automatically invoke a Cloud Function in an specific schedule.
