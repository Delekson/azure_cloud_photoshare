from azure.storage.blob import BlobServiceClient, generate_blob_sas
import datetime as dt
import sys
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from config.config_files import APIkeys

class accounts:
    def __init__(self, key, account):
        self.account_name = account
        self.private_key = key
        account_url = f"https://{account}.blob.core.windows.net"
        self.blob_service_client = BlobServiceClient(account_url, credential=self.private_key)

class containers(accounts):
    def __init__(self, key, account, container_name):
        super().__init__(key, account)
        self.container_client = self.blob_service_client.get_container_client(container_name)

class blobs(containers):
    def __init__(self, key, account, container_name, blob_name):
        super().__init__(key, account, container_name)
        self.blob_name = blob_name
        self.blob_client = self.container_client.get_blob_client(blob=blob_name)

    def upload(self, file_path):
        with open(file=file_path, mode="rb") as data:
            self.blob_client.upload_blob(data)
    
    def share_link(self, policy):
        sas = generate_blob_sas(account_name=self.account_name, container_name=self.container_client.container_name, blob_name=self.blob_name, start = dt.datetime.now(), expiry=dt.datetime.now() + dt.timedelta(days=1), account_key = self.private_key, policy_id=policy)
        self.link = f"{self.blob_client.primary_endpoint}?{sas}"
        return self.link

class apps(QDialog):
    def __init__(self, parent=None):
        super(apps, self).__init__(parent)

        self.to_upload_button_obj = QPushButton("Select image to upload")
        self.file_path_text = QLineEdit("File path of to upload file")
        self.file_path_text.setReadOnly(True)

        self.upload_button_obj = QPushButton("Share image")
        self.blob_name_text = QLineEdit("Set blob name")

        self.share_link_text = QLineEdit("Your shareable link")
        self.share_link_text.setReadOnly(True)
        self.copy_sl = QPushButton("")
        
        icon = QIcon("config\copy_icon.png")
        self.copy_sl.setIcon(icon)
        self.copy_sl.setIconSize(QSize(24,24))

        layout = QVBoxLayout()
        layout.addWidget(self.to_upload_button_obj)
        layout.addWidget(self.file_path_text)
        layout.addWidget(self.blob_name_text)
        layout.addWidget(self.upload_button_obj)
        layout.addWidget(self.share_link_text)
        layout.addWidget(self.copy_sl)

        layout.setAlignment(self.copy_sl, Qt.AlignCenter)
        self.setLayout(layout)

        self.copy_sl.clicked.connect(self.copy_to_cb_button)
        self.to_upload_button_obj.clicked.connect(self.to_upload_button)
        self.upload_button_obj.clicked.connect(self.upload_button)

    def to_upload(self):
        self.file_path = QFileDialog.getOpenFileName(caption="Open File",dir="/home",filter="Images (*.png *.xpm *.jpg)")[0]
        self.file_name = self.file_path[self.file_path.rfind("/")+1:]
        self.file_extension = self.file_path[self.file_path.rfind(".")+1:]

    def to_upload_button(self):
        self.to_upload()
        self.file_path_text.setText(self.file_path)
        self.file_path_text.setReadOnly(True)

    def upload_button(self):
        self.blob_name = f"{self.blob_name_text.text()}.{self.file_extension}"
        blob = blobs(APIkeys.private_key, "udemydemostgacc", "photostoredm", self.blob_name)
        blob.upload(self.file_path)
        self.share_link = blob.share_link("shared")
        self.share_link_text.setText(self.share_link)
        self.share_link_text.setReadOnly(True)
    
    def copy_to_cb_button(self):
        clipboard = QClipboard()
        clipboard.setText(self.share_link_text.text())

if __name__ == '__main__':
    # Create the Qt Application
    app_init = QApplication(sys.argv)
    form = apps()
    form.show()
    sys.exit(app_init.exec())