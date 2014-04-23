from flask import Flask, request, redirect, url_for
from flask.templating import render_template
from flask import url_for
# from util import unigram_features, bigram_features
import nltk
import re
import json
import random
import os 
import string
import csv
import codecs
import pickle
from collections import OrderedDict
from career_trajectory_svm_new_0416 import unigram_features, bigram_features, tfidftransform
global flag
flag = 1



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
    uni_feats = [" ".join(unigram_features(resume_text, top_unigram_list))]
    bi_feats = [" ".join(bigram_features(resume_text, top_bigram_list))]
    consolidated_features = []
    ind = 0
    while ind < len(uni_feats):
        consolidated_features.append(uni_feats[ind] + bi_feats[ind])
        ind += 1
    return consolidated_features

@app.route('/')
def hello_world():
    global flag
    print"main page"
    print flag
    return render_template('index_result.html', flag = flag)



@app.route("/analyze", methods=['POST','GET'])
def analyze():
    global flag
    if request.method:
        flag =1
        # Get and save file from browser upload
        file = request.files['file']
        if file :
            filename = file.filename
            print filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # f = codecs.open(filename)
            # raw = f.read()
            # raw = unicode(raw, errors='ignore')
            resume_text = [open(filename).read()]

    # Get the pickled classifier model and features
    with open('svmclassifier_new_0420_hash.pkl', 'rb') as infile:
        model = pickle.load(infile)

    with open('label_names_0420_hash.pkl', 'rb') as lab_names:
        labels_names = pickle.load(lab_names)

    with open('hash_vect_0420_hash.pkl', 'rb') as hash_v:
        hash_vect = pickle.load(hash_v)

    resume_hash = hash_vect.transform(resume_text)
    predicted_score = model.predict(resume_hash)
    predicted_decision = model.decision_function(resume_hash)

    predicted = []

    for i in range(1):
        predicted_dec_dup = predicted_decision[i]
        predicted_dec_dup_sorted = sorted(predicted_dec_dup, reverse=True)
        top_five_predictions = []
        predicted.append(labels_names[predicted_decision[i].tolist().index(predicted_dec_dup_sorted[0])])
        for j in range(5):
            top_five_predictions.append(labels_names[predicted_decision[i].tolist().index(predicted_dec_dup_sorted[j])])

        print "Predicted top5: " + ", ".join(top_five_predictions)


# hard coding responses for now
    out = {}
    # top_five_predictions =["VP","Director","Senior Manager","Senior Consultant","CEO"]
    top_five_predictions_caps = [string.capwords(tfp) for tfp in top_five_predictions]
    out["predicted"] = top_five_predictions_caps
    out["employer"] = ["deloitte","salesforce","yahoo"]
    out["title"] = ["UX Designer","Software engineer","Consultant"]

    skills_map_with_percent = json.loads(open("skills_map_with_percent.json").read())
    skills_map_with_percent_list = []
    for pred in top_five_predictions:
        temp_skill_map = dict()
        temp_skill_map[string.capwords(pred)] = skills_map_with_percent[pred]
        skills_map_with_percent_list.append(temp_skill_map)

    out["skills_map"] = skills_map_with_percent_list

    return json.dumps(OrderedDict(out))
 
    


    
if __name__ == '__main__':
    app.run()
    # url_for('static', filename='*.txt')
    # url_for('static', filename='*.png')




