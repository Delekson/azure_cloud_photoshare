'''
Main python file that is ran to launch the app.
'''
import datetime as dt
import sys

from azure.storage.blob import BlobServiceClient, generate_blob_sas
import PySide6.QtCore as core
import PySide6.QtGui as gui
import PySide6.QtWidgets as widget

import config_files as config


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


class Forms(widget.QDialog):
    '''
    The Forms class houses everything to do with the front end of the app.
    '''
    def __init__(self, parent=None):
        super(Forms, self).__init__(parent)
        # file selection button
        self.to_upload_button_obj = widget.QPushButton("Select image to upload")
        self.file_path_text = widget.QLineEdit("File path of to upload file")
        self.file_path_text.setReadOnly(True)
        self.to_upload_button_obj.clicked.connect(self.to_upload_button)
        self.file_path = None
        self.file_name = None
        self.file_extension = None
        # blob upload section
        self.upload_button_obj = widget.QPushButton("Share image")
        self.blob_name_text = widget.QLineEdit("Set blob name")
        self.upload_button_obj.clicked.connect(self.upload_button)
        self.blob_name = None
        # share link section
        self.share_link_text = widget.QLineEdit("Your shareable link")
        self.share_link_text.setReadOnly(True)
        self.share_link = None
        # copy and paste button for share link
        self.copy_sl = widget.QPushButton("")
        icon = gui.QIcon(r"resources\copy_icon.png")
        self.copy_sl.setIcon(icon)
        self.copy_sl.setIconSize(core.QSize(24, 24))
        self.copy_sl.clicked.connect(self.copy_to_cb_button)
        # layouts
        layout = widget.QVBoxLayout()
        layout.addWidget(self.to_upload_button_obj)
        layout.addWidget(self.file_path_text)
        layout.addWidget(self.blob_name_text)
        layout.addWidget(self.upload_button_obj)
        layout.addWidget(self.share_link_text)
        layout.addWidget(self.copy_sl)
        self.setLayout(layout)

    def to_upload(self):
        '''
        This fuction allows the user to open a file dialog to select what image
        they want to share.
        '''
        self.file_path = widget.QFileDialog.getOpenFileName(
            caption="Open File", dir = core.QDir.homePath(),
                filter = "Images (*.png *.xpm *.jpg)")[0]
        self.file_name = self.file_path[self.file_path.rfind("/")+1:]
        self.file_extension = self.file_path[self.file_path.rfind(".")+1:]

    def to_upload_button(self):
        '''
        This function houses the function passed to the button: select file
        prompt, updates text underneath with file path.
        '''
        self.to_upload()
        self.file_path_text.setText(self.file_path)
        self.file_path_text.setReadOnly(True)

    def upload_button(self):
        '''
        This function houses the function passed to the button: takes blob name
        input, sets up a blob client, uploads to the cloud and generates a
        share link (updating the text below).
        '''
        self.blob_name = f"{self.blob_name_text.text()}.{self.file_extension}"
        blob = Blobs(config.vars.private_key, config.vars.account_name,
                     config.vars.container_name, self.blob_name)
        blob.upload(self.file_path)
        self.share_link = blob.share_link("shared")
        self.share_link_text.setText(self.share_link)
        self.share_link_text.setReadOnly(True)

    def copy_to_cb_button(self):
        '''
        This function houses the function passed to the copy to clipboard
        button which essentially copies the share link to the user's
        clipboard
        '''
        clipboard = gui.QClipboard()
        clipboard.setText(self.share_link_text.text())


if __name__ == '__main__':
    # Create the Qt Application
    app_init = widget.QApplication(sys.argv)
    form = Forms()
    form.show()
    sys.exit(app_init.exec())