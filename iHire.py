from flask import Flask, request
from flask.templating import render_template
from flask import url_for
import nltk
import re
import json
import random
import os 
import string
import csv



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = ""
app.debug="true"

@app.route('/')
def hello_world():
    print"main page"
    return render_template('index.html')


@app.route("/analyze", methods=['POST'])
def analyze():
    print "analyze"
    if request.method:
        file = request.files.getlist('file')[0]
        if file :
            filename = file.filename
            print filename
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            rand = ''.join(random.choice(string.ascii_uppercase) for i in range(12))

            with open(filename, 'rU') as csv_file:
                reader = csv.reader(csv_file)
                header = reader.next()

            response = {'update': rand, 'filename': filename, 'header': header}


            return json.dumps(response)
    

    
if __name__ == '__main__':
    app.run()
    # url_for('static', filename='*.txt')
    # url_for('static', filename='*.png')




