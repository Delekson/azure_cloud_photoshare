from azure.storage.blob import BlobServiceClient, generate_blob_sas
import datetime as dt
import sys
from PySide6.QtWidgets import QApplication, QPushButton, QFileDialog, QVBoxLayout, QDialog, QLineEdit
from config.config_files import APIkeys

class accounts:
    def __init__(self, key, account):
        self.account_name = account
        self.private_key = key
        account_url = f"https://{account}.blob.core.windows.net"
        self.blob_service_client = BlobServiceClient(account_url, credential=self.private_key)

class containers:
    def __init__(self, account_class, container_name):
        self.account = account_class
        self.container_client = self.account.blob_service_client.get_container_client(container_name)

class blobs:
    def __init__(self, container_class, blob_name):
        self.account = container_class.account
        self.container = container_class
        self.blob_name = blob_name
        self.blob_client = container_class.container_client.get_blob_client(blob=blob_name)

    def upload(self, file_path):
        with open(file=file_path, mode="rb") as data:
            self.blob_client.upload_blob(data)
    
    def share_link(self, policy):
        sas = generate_blob_sas(account_name=self.account.account_name, container_name=self.container.container_client.container_name, blob_name=self.blob_name, start = dt.datetime.now(), expiry=dt.datetime.now() + dt.timedelta(days=1), account_key = self.account.private_key, policy_id=policy)
        url_file_name = self.blob_name.replace(" ","%20")

        self.link = f"https://{self.account.account_name}.blob.core.windows.net/{self.container.container_client.container_name}/{url_file_name}?{sas}"
        return self.link

class apps(QDialog):
    def __init__(self, parent=None):
        super(apps, self).__init__(parent)

        self.account = accounts(APIkeys.private_key, "udemydemostgacc")
        self.container = containers(self.account, "photostoredm")

        self.to_upload_button_obj = QPushButton("Select image to upload")
        self.file_path_text = QLineEdit("File path of to upload file")
        self.file_path_text.isReadOnly = True

        self.upload_button_obj = QPushButton("Share image")
        self.blob_name_text = QLineEdit("Set blob name")
        self.share_link_text = QLineEdit("Your shareable link")
        self.share_link_text.isReadOnly = True

        layout = QVBoxLayout()
        layout.addWidget(self.to_upload_button_obj)
        layout.addWidget(self.file_path_text)
        layout.addWidget(self.upload_button_obj)
        layout.addWidget(self.blob_name_text)
        layout.addWidget(self.share_link_text)
        self.setLayout(layout)

        self.to_upload_button_obj.clicked.connect(lambda: self.to_upload_button())
        self.upload_button_obj.clicked.connect(lambda: self.upload_button(self.account, self.container))

    def to_upload(self):
        self.file_path = QFileDialog.getOpenFileName(caption="Open File",dir="/home",filter="Images (*.png *.xpm *.jpg)")[0]
        self.file_name = self.file_path[self.file_path.rfind("/")+1:]

    def to_upload_button(self):
        self.to_upload()
        self.file_path_text.setText(self.file_path)

    def upload_button(self, account_class, container_class):
        self.blob_name = self.blob_name_text.text()
        blob = blobs(container_class, self.blob_name)
        blob.upload(self.file_path)
        self.share_link = blob.share_link("shared")
        self.share_link_text.setText(self.share_link)

if __name__ == '__main__':
    # Create the Qt Application
    app_init = QApplication(sys.argv)
    form = apps()
    form.show()
    sys.exit(app_init.exec())