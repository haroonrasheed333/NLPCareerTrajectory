# from util import unigram_features, bigram_features
import os
import re
import csv
import nltk
import json
import random
import string
import codecs
import pickle
import numpy as np
from cStringIO import StringIO
from collections import OrderedDict
from flask.templating import render_template
from flask import Flask, request, redirect, url_for
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from career_trajectory_svm_new_0416 import unigram_features, bigram_features, tfidftransform
from univ_lookup import extract_univ
from Marisa import get_degree_level_from_resume, get_degree


global flag
global university
university = 'University of California Berkeley'
flag = 1

iHire = Flask(__name__)
iHire.config['UPLOAD_FOLDER'] = ""
iHire.debug="true"

# Get the pickled classifier model and features
with open('svmclassifier_new_0420_marisa.pkl', 'rb') as infile:
    model = pickle.load(infile)

with open('label_names_0420_marisa.pkl', 'rb') as lab_names:
    labels_names = pickle.load(lab_names)

with open('tfidf_vect_0420_marisa.pkl', 'rb') as hash_v:
    tfidf_vect = pickle.load(hash_v)

title_title_map = json.loads(open("title_title_map.json").read())

skills_map_with_percent = json.loads(open("skills_map_with_percent_new_0429_upper.json").read())


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


def extract_text_from_pdf(pdf_filename):
    # os.system("pdftotext -layout " + filename)

    resource_manager = PDFResourceManager()
    return_string = StringIO()
    la_params = LAParams()
    device = TextConverter(resource_manager, return_string, codec='utf-8', laparams=la_params)
    fp = file(pdf_filename, 'rb')
    interpreter = PDFPageInterpreter(resource_manager, device)
    page_nos = set()

    for page in PDFPage.get_pages(fp, page_nos):
        interpreter.process_page(page)
    fp.close()

    device.close()
    extracted_text = return_string.getvalue()
    return_string.close()

    return extracted_text


@iHire.route('/')
def hello_world():
    global flag
    print"main page"
    print flag
    return render_template('index_result.html', flag = flag)

@iHire.route('/network')
def network():
    return render_template('network.html', parameter = university)

@iHire.route("/analyze", methods=['POST','GET'])
def analyze():
    global flag
    if request.method:
        flag =1
        # Get and save file from browser upload
        files = request.files['file']
        if files:
            filename = str(files.filename)
            print filename
            extension = filename.rsplit('.', 1)[1]
            filename_without_extension = filename.rsplit('.', 1)[0]
            files.save(os.path.join(iHire.config['UPLOAD_FOLDER'], filename))

            if extension == 'pdf':
                text_from_pdf = extract_text_from_pdf(filename)
                with open(filename_without_extension + '.txt', 'wb') as write_file:
                    write_file.write(text_from_pdf)

                textfile_name = filename_without_extension + '.txt'
            else:
                textfile_name = filename

            print filename
            resume_text = [open(filename).read()]

            global university
            university = extract_univ(open(textfile_name).read())
            print university


            resume_text = [open(textfile_name).read()]

            resume_tfidf = tfidf_vect.transform(resume_text)
            # resume_tfidf_array = resume_tfidf.toarray()
            # resume_degree_level = np.array([get_degree_level_from_resume([(resume_text[0], '', '')])])
            # print resume_degree_level
            # resume_tfidf_array_degree_level = np.concatenate((resume_tfidf_array, resume_degree_level.T), axis=1)


            predicted_score = model.predict(resume_tfidf)
            predicted_decision = model.decision_function(resume_tfidf)

            predicted = []

            for i in range(1):
                predicted_dec_dup = predicted_decision[i]
                predicted_dec_dup_sorted = sorted(predicted_dec_dup, reverse=True)
                top_five_predictions = []
                predicted.append(labels_names[predicted_decision[i].tolist().index(predicted_dec_dup_sorted[0])])
                for j in range(5):
                    top_five_predictions.append(
                        labels_names[predicted_decision[i].tolist().index(predicted_dec_dup_sorted[j])]
                    )

                print "Predicted top5: " + ", ".join(top_five_predictions)

            # hard coding responses for now
            out = dict()
            top_five_predictions_caps = [title_title_map[tfp] for tfp in top_five_predictions]
            out["predicted"] = top_five_predictions_caps
            out["employer"] = ["Deloitte","Sales Force","Yahoo"]
            out["title"] = ["UX Designer", "Software engineer", "Consultant"]
            out["university"] = university

            skills_map_with_percent_list = []
            for pred in top_five_predictions:
                temp_skill_map = dict()
                temp_skill_map[title_title_map[pred]] = skills_map_with_percent[title_title_map[pred]]
                skills_map_with_percent_list.append(temp_skill_map)

            out["skills_map"] = skills_map_with_percent_list

            if os.path.isfile(textfile_name):
                    os.remove(textfile_name)

            if os.path.isfile(filename):
                    os.remove(filename)

            return json.dumps(OrderedDict(out))
    
if __name__ == '__main__':
    iHire.run(host='0.0.0.0')




