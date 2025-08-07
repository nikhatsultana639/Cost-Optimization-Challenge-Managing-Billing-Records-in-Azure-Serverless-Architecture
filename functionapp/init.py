import datetime
import azure.functions as func
from azure.cosmos import CosmosClient
from azure.storage.blob import BlobServiceClient
import json
import os

COSMOS_URL = os.environ["COSMOS_URL"]
COSMOS_KEY = os.environ["COSMOS_KEY"]
DATABASE_NAME = os.environ["COSMOS_DB"]
CONTAINER_NAME = os.environ["COSMOS_CONTAINER"]

BLOB_CONN_STR = os.environ["BLOB_CONN_STR"]
BLOB_CONTAINER = os.environ["BLOB_CONTAINER"]

def main(mytimer: func.TimerRequest) -> None:
    client = CosmosClient(COSMOS_URL, COSMOS_KEY)
    container = client.get_database_client(DATABASE_NAME).get_container_client(CONTAINER_NAME)
    
    three_months_ago = (datetime.datetime.utcnow() - datetime.timedelta(days=90)).isoformat()
    query = f'SELECT * FROM c WHERE c.timestamp < "{three_months_ago}"'

    blob_service = BlobServiceClient.from_connection_string(BLOB_CONN_STR)
    container_client = blob_service.get_container_client(BLOB_CONTAINER)

    for item in container.query_items(query=query, enable_cross_partition_query=True):
        blob_name = f"{item['id']}.json"
        container_client.upload_blob(name=blob_name, data=json.dumps(item), overwrite=True, standard_blob_tier="Cool")

        # Optionally delete after backup
        # container.delete_item(item, partition_key=item['partitionKey'])
