from flask import Flask, jsonify, render_template, request
import main
import config_files as config

app = Flask(__name__)

container_blob = main.Containers(config.vars.private_key, config.vars.account_name,
                     config.vars.container_name)

@app.route("/")
def Blob_list():
    return render_template('home_page.html', container=container_blob.list_blobs())

@app.route('/generatelink')
def Generatelink():
    blob_name = request.args.get('blob')
    blob_client = main.Blobs(container_blob.private_key, container_blob.account_name,
                     container_blob.container_name, blob_name)
    share_link = blob_client.share_link("shared")
    return share_link

if __name__ == '__main__':
    app.run(debug=True)