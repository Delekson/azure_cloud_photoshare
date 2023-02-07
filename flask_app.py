from flask import Flask, jsonify, render_template, request
import flask_main
import config_files as config

app = Flask(__name__)


@app.route("/")
def Blob_list():
    '''
    This route renders all the blobs that are uploaded to the storage account
    '''
    return render_template('home_page.html', container=container_blob.list_blobs())

@app.route('/generatelink')
def Generatelink():
    '''
    This api request returns the share link of a specified blob which is passed as a request param named blob
    '''
    blob_name = request.args.get('blob')
    blob_client = flask_main.Blobs(container_blob.private_key, container_blob.account_name,
                     container_blob.container_name, blob_name)
    share_link = blob_client.share_link("shared")
    return share_link

if __name__ == '__main__':
    container_blob = flask_main.Containers(config.vars.private_key, config.vars.account_name,
                                       config.vars.container_name)
    app.run(debug=True)