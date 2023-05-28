import os
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
load_dotenv()

storage_account_key = os.environ.get('STORAGE_KEY')
storage_account_name = os.environ.get('STORAGE_NAME')
connection_string = os.environ.get('STORAGE_CONN')
container_name_in = "input-files"
container_name_out = "output-files"


def upload_blob(file_path, file_name):
    """
    Upload a file to input-files container
    :param file_path: location of the file to upload
    :param file_name: name of the file in the container
    :return: None
    """
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name_in, blob=file_name)
    with open(file_path, "rb") as data:
        blob_client.upload_blob(data)
        print(f"Uploaded {file_name}.")


def download_blob(file_path, file_name):
    """
    Download a file from output-files container
    :param file_path: location to download the file
    :param file_name: name of the file in the container
    :return: None
    """
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name_out, blob=file_name)
    with open(file_path, "wb") as data:
        download_stream = blob_client.download_blob()
        data.write(download_stream.readall())


def delete_blob(file_name, container='in'):
    """
    Delete a file from the specified container
    :param file_name: name of the file in the container
    :param container: container to delete from. can be 'in' or 'out'
    :return: None
    """
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    if container == 'in':
        blob_client = blob_service_client.get_blob_client(container=container_name_in, blob=file_name)
    elif container == 'out':
        blob_client = blob_service_client.get_blob_client(container=container_name_out, blob=file_name)
    else:
        pass
    blob_client.delete_blob()


def write2txt(input_file, file_path):
    with open(file_path, 'w', encoding='utf-8') as doc:
        doc.write(input_file)


def input2wav(input_file, file_path):
    with open(file_path, mode='bx') as doc:
        doc.write(input_file)
