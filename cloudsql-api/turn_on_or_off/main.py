from pprint import pprint
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
import os

credentials = GoogleCredentials.get_application_default()
service = discovery.build("sqladmin", "v1beta4", credentials=credentials)
project_id = os.environ.get("GCP_PROJECT")

# setup this vars using terraform and assign the value via terraform
desired_policy = os.environ.get("DESIRED_POLICY") # ALWAYS or NEVER
instance_name = os.environ.get("INSTANCE_NAME")

def cloudsql(request):
    request = service.instances().get(project=project_id, instance=instance_name)
    response = request.execute()

    state = response["state"]
    instance_state = str(state)

    x = response["settings"]
    current_policy = str(x["activationPolicy"])

    dbinstancebody = {"settings": {"activationPolicy": desired_policy}}


    if instance_state != "RUNNABLE":
        print("Instance is not in RUNNABLE STATE")
    else:
        if desired_policy != current_policy:
            request = service.instances().patch(
                project=project_id, instance=instance_name, body=dbinstancebody
            )
            response = request.execute()

            pprint(response)
        else:
            print(f"Instance is in RUNNABLE STATE but is also already configured with the desired policy: {desired_policy}")
