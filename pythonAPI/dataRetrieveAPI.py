from azure.cosmos import CosmosClient
from azure.storage.blob import BlobServiceClient
import os
import json

def get_record(record_id):
    try:
        # Try Cosmos
        cosmos_client = CosmosClient(os.environ["COSMOS_URL"], os.environ["COSMOS_KEY"])
        container = cosmos_client.get_database_client(os.environ["COSMOS_DB"]).get_container_client(os.environ["COSMOS_CONTAINER"])
        item = container.read_item(item=record_id, partition_key=record_id)
        return item
    except:
        # Fallback to Blob Storage
        blob_service = BlobServiceClient.from_connection_string(os.environ["BLOB_CONN_STR"])
        blob_client = blob_service.get_container_client(os.environ["BLOB_CONTAINER"]).get_blob_client(f"{record_id}.json")
        blob_data = blob_client.download_blob().readall()
        return json.loads(blob_data)
