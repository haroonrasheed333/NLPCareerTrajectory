from flask import Flask, request, redirect, url_for
from flask.templating import render_template
from flask import url_for
from util import unigram_features, bigram_features
import nltk
import re
import json
import random
import os 
import string
import csv
import codecs
import pickle



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = ""
app.debug="true"


def feature_consolidation(resume_text, top_unigram_list, top_bigram_list):
    """
    Function to consolidate all the featuresets for the training data

    Args:
        top_unigram_list -- list of top unigrams from the training dataset
        top_bigram_list -- list of top bigrams from the training dataset

    Returns:
        consolidated_features -- list of consolidated features
    """
    uni_feats = [unigram_features(resume_text, top_unigram_list)]
    bi_feats = [bigram_features(resume_text, top_bigram_list)]
    consolidated_features = []
    ind = 0
    while ind < len(uni_feats):
        consolidated_features.append(uni_feats[ind] + bi_feats[ind])
        ind += 1
    return consolidated_features

@app.route('/')
def hello_world():
    print"main page"
    return render_template('index.html')


@app.route("/analyze", methods=['POST','GET'])
def analyze():
    if request.method:
        # Get and save file from browser upload
        file = request.files['file']
        if file :
            filename = file.filename
            print filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            f = codecs.open(filename)
            raw = f.read()
            raw = unicode(raw, errors='ignore')

    # Get the pickled classifier model and features
    with open('svmclassifier_new_0416.pkl', 'rb') as infile:
        model = pickle.load(infile)

    with open('features.pkl', 'rb') as f:
        features = pickle.load(f)

    with open('label_names.pkl', 'rb') as lab_names:
        labels_names = pickle.load(lab_names)

    top_unigrams = features['top_unigrams']
    top_bigrams = features['top_bigrams']

    resume_text = raw

    # Create a featureset for the heldout data
    resume_featureset = feature_consolidation(resume_text, top_unigrams, top_bigrams)

    predicted_score = model.predict(resume_featureset)
    predicted_decision = model.decision_function(resume_featureset)

    predicted = []

    for i in range(1):
        predicted_dec_dup = predicted_decision[i]
        predicted_dec_dup_sorted = sorted(predicted_dec_dup, reverse=True)
        top_five_predictions = []
        predicted.append(labels_names[predicted_decision[i].tolist().index(predicted_dec_dup_sorted[0])])
        for j in range(5):
            top_five_predictions.append(labels_names[predicted_decision[i].tolist().index(predicted_dec_dup_sorted[j])])

        print "Predicted top5: " + ", ".join(top_five_predictions)

    out ={}
    top_five_predictions =["1","2","3","4","5"]
    out["predicted"] = top_five_predictions
    out["employer"] = ["deloitte","salesforce","yahoo"]
    out["title"] = ["UX Designer","Software engineer","Consultant"]

    return json.dumps(out)
 
    


    
if __name__ == '__main__':
    app.run()
    # url_for('static', filename='*.txt')
    # url_for('static', filename='*.png')




