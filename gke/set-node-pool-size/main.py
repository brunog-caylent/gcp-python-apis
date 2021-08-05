from pprint import pprint
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
import os

# https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1/projects.locations.clusters.nodePools/setSize

credentials = GoogleCredentials.get_application_default()
service = discovery.build("container", "v1", credentials=credentials)
project_id = os.environ.get("GCP_PROJECT")

# setup this vars using terraform and assign the value via terraform
location = os.environ.get("CLUSTER_LOCATION")
cluster_name = os.environ.get("CLUSTER_NAME")
node_pool = os.environ.get("NODE_POOL_NAME")
desired_node_count = int(os.environ.get("DESIRED_NODE_COUNT"))


def set_node_pool_size(request):
    # Specified in the format 'projects/*/locations/*/clusters/*/nodePools/*'.
    name = f"projects/{project_id}/locations/{location}/clusters/{cluster_name}/nodePools/{node_pool}"

    request = service.projects().locations().clusters().nodePools().get(name=name)
    response = request.execute()

    status = response["status"]
    node_pool_status = str(status)

    if node_pool_status == "RUNNING":
        updated_body = {"nodeCount": desired_node_count}
        request = (
            service.projects()
            .locations()
            .clusters()
            .nodePools()
            .setSize(name=name, body=updated_body)
        )

        response = request.execute()

        pprint(response)
    else:
        print("NodePool is not in RUNNING STATE")
