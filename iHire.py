from flask import Flask, request
from flask.templating import render_template
from flask import url_for
import nltk
import re
import json
import random
import os 
import string
from cluster import Cluster


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = ""

@app.route('/')
def hello_world():
    return render_template('index.html')
#
@app.route('/file-upload', methods=['POST'])
def upload_file():
    responses = []
    files = request.files.getlist('file')
    for file in files:
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            rand = ''.join(random.choice(string.ascii_uppercase) for i in range(12))
            response = {'update': rand, 'filename': filename}
            responses.append(response)
    return json.dumps(responses)

@app.route('/cluster', methods=['POST'])
def cluster():
    parameters=request.json['parameters']
    clusterflag = request.json['recluster']
    algorithm = parameters["algorithm"]
    if clusterflag ==0:
        fileNames = request.json['filename']
        clusterObj = Cluster(len(fileNames) -1, parameters)
        clusterObj.loadCorpus(fileNames)

    if algorithm == "Non Negative Matrix Factorization":
        return clusterObj.nmf()
    elif algorithm == "Latent Dirichlet Allocation":
        return clusterObj.lda()
    else:
        return clusterObj.nmf()

    
if __name__ == '__main__':
    app.run()
    url_for('static', filename='*.txt')
    url_for('static', filename='*.png')




