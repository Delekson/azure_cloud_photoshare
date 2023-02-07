from flask import Flask, jsonify, render_template, request, flash, redirect, session
import flask_main
import config_files as config
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route("/")
def home():
    '''
    This route renders the home page linking all sub pages of the app
    '''
    return render_template('home.html')

@app.route("/list_uploads")
def list_upload():
    '''
    This route renders all the blobs that are uploaded to the storage account
    '''
    return render_template('list_uploads.html', container=container_blob.list_blobs())

@app.route('/generatelink')
def generate_link():
    '''
    This request returns the share link of a specified blob which is passed as a request
    param named blob
    '''
    blob_name = request.args.get('blob')
    blob_client = flask_main.Blobs(container_blob.private_key, container_blob.account_name,
                     container_blob.container_name, blob_name)
    share_link = blob_client.share_link("shared")
    return share_link

@app.route('/upload', methods = ['GET', 'POST'])
def upload_home():
    '''
    This route renders the page where user uploads the blob
    '''
    if request.method == 'POST':
        blob_name = request.form['blob_name']
        file = request.files['file']
        if 'file' not in request.files:
            flash('No file part')
        elif file.filename == '':
            flash('Please select an image file.')
        elif "image" not in file.content_type:
            flash('Please select an image file (png or jpg/jpeg).')
        elif blob_name in container_blob.list_blobs():
            flash('Image name already exists. Please resubmit with a different name.')
        else:
            blob_client = flask_main.Blobs(container_blob.private_key, container_blob.account_name,
                     container_blob.container_name, blob_name)
            blob_client.upload(file)
            flash('File Uploaded!')
        return redirect(request.url)
    return render_template('upload.html')

if __name__ == '__main__':

    container_blob = flask_main.Containers(config.vars.private_key, config.vars.account_name,
                                       config.vars.container_name)
    app.secret_key = config.vars.secret_key
    app.run(debug=True)