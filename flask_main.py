'''
Main python file that is ran to launch the app.
'''
import datetime as dt
import sys
import os

from azure.storage.blob import BlobServiceClient, generate_blob_sas

class Accounts:
    '''
    The Accounts class houses the client used to connect the storage account
    on Azure Storage
    '''
    def __init__(self, key, account):
        self.account_name = account
        self.private_key = key
        account_url = f"https://{account}.blob.core.windows.net"
        self.blob_service_client = BlobServiceClient(
            account_url, credential=self.private_key)


class Containers(Accounts):
    '''
    The Containers class houses the client used to connect a specified
    container inside the parent Accounts class storage account on Azure Storage
    '''
    def __init__(self, key, account, container_name):
        super().__init__(key, account)
        self.container_name = container_name
        self.container_client = self.blob_service_client.get_container_client(
            container_name)

    def list_blobs(self):
        '''
        Returns a list of blob names stored inside the container.
        '''
        return self.container_client.list_blob_names()


class Blobs(Containers):
    '''
    The Blobs class houses the client used to 'connect' a specified
    blob of a given name inside the parent Containers class on Azure Storage
    '''
    def __init__(self, key, account, container_name, blob_name):
        super().__init__(key, account, container_name)
        self.blob_name = blob_name
        self.blob_client = self.container_client.get_blob_client(
            blob=blob_name)
        self.link = None

    def upload(self, file_path):
        '''
        Uploads the selected file to the connected container named as a given
        blob name during Blobs class init.
        '''
        with open(file=file_path, mode="rb") as data:
            self.blob_client.upload_blob(data)

    def share_link(self, policy):
        '''
        Generates a sas link to the file with read only permission
        '''
        sas = generate_blob_sas(account_name=self.account_name,
            container_name=self.container_client.container_name,
                blob_name=self.blob_name, start=dt.datetime.now(),
                    expiry=dt.datetime.now() + dt.timedelta(days=1),
                        account_key=self.private_key, policy_id=policy)
        self.link = f"{self.blob_client.primary_endpoint}?{sas}"
        return self.link