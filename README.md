#azure_cloud_photoshare
This app uses the Azure Blob Python SDK to provide photosharing functionality.

##Current Set-Up
This code relies on on the following modules: datetime which is pre-installed. sys which is pre-installed. azure.storage.blob installed using pip install azure-storage-blob. PySide6 installed using pip install PySide6.

You will also need to have set up an Azure Service Account with a storage account along with a blob container within that storage account (and permission to make changes to the storage account via an access key).

This app requires a file in the main directory named ".env" with the following content:

```
account_key=<shared key or access key to storage account>
account_name=<account name>
container_name=<container name>
```
##Future Possible Features
My to do list to take the app further (features may or not be developed due to time constraints and resourcing availability): 
+Better front-end by potentially using AirBnB guidelines or Material-Ui esque 
+Accounts (general idea being a container per user) 
+Robust way of storing authentication information 
+Ability to view image once image file is selected 
+Ability to see existing images +Ability to regenerate share links to existing images 
+Ability to manage images more specifically ability to delete and undelete 
+Look into making code more efficient 
+Url shortening for share_link
