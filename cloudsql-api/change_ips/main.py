from pprint import pprint
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
import os

credentials = GoogleCredentials.get_application_default()
service = discovery.build("sqladmin", "v1beta4", credentials=credentials)

# if cloud function python version is 37 you dont need to define this var, if it is a newer version you have to add the var via terraform or manually though
project_id = os.environ.get("GCP_PROJECT")

# setup this var using terraform and assign the value via terraform
instance_name = os.environ.get("INSTANCE_NAME")

def cloudsql_ip(request):
    request = service.instances().get(project=project_id, instance=instance_name)
    response = request.execute()

    # A list of dict to pass the values. Although it only has name and value,
    # other accepeted values are: "expirationTime" and "kind"(which is always :"sql#aclEntry")
    ips_and_names = [
        {"name": "example1", "value": "0.0.0.0/0"},
        {"name": "example2", "value": "0.0.0.0/0"},
    ]

    authorized_networks = {"authorizedNetworks": ips_and_names}

    dbinstancebody = {"settings": {"ipConfiguration": authorized_networks}}

    request = service.instances().patch(
                project=project_id, instance=instance_name, body=dbinstancebody
            )
    response = request.execute()

    pprint(response)
