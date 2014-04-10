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


@app.route('/analyze', methods=['POST'])
def analyze():  



    
if __name__ == '__main__':
    app.run()
    url_for('static', filename='*.txt')
    url_for('static', filename='*.png')




