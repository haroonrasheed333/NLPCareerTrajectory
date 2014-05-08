import os
import re
import csv
import nltk
import json
import string
import pickle
from cStringIO import StringIO
from collections import OrderedDict
from flask.templating import render_template
from flask import Flask, request, redirect, url_for
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from univ_lookup import extract_univ

from univ_lookup import create_data_for_graph
from univ_lookup import create_data_for_tree


# global flag
# global university
# global results_json
results_json = dict()
university = ''
flag = 1

#Create Flask instance
iHire = Flask(__name__)
iHire.config['UPLOAD_FOLDER'] = ""
iHire.debug = "true"

# Get the pickled classifier model and features
with open('iBeyond_classifier.pkl', 'rb') as infile:
    model = pickle.load(infile)

with open('iBeyond_labels.pkl', 'rb') as lab_names:
    labels_names = pickle.load(lab_names)

# with open('tfidf_vect_0420_marisa.pkl', 'rb') as hash_v:
#     tfidf_vect = pickle.load(hash_v)

title_title_map = json.loads(open("title_title_map.json").read())
skills_map_with_percent = json.loads(open("skills_map_with_percent_new_0504_upper.json").read())
univ_dict = json.loads(open("static/univs_list.json","rb").read())
univ_normalize = json.loads(open("static/univ_map.json","rb").read())
skills_employer = json.loads(open("static/networkgraph.json").read())
skills_employer_tree = json.loads(open("static/treegraphdata.json").read())
univ_major_number = json.loads(open("static/univ_mapping.json").read())
major_code_lookup = json.loads(open("static/DeptCodes.json").read())

titles_data = json.loads(open("titlesData_new.json").read())


def extract_text_from_pdf(pdf_filename):
    """
    Function to extract the text from pdf documents using pdfminer

    Args:
        pdf_filename -- File name of the pdf document as string

    Returns:
        extracted_text -- Extracted text as string
    """
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


def get_top_predictions(predicted_decision):
    """
    Function to find the top predictions and compute scores based on the svm classifier decisions

    Args:
        predicted_decision -- list of svm prediction decisions

    Returns:
        top_five_predictions, normalized_prediction_score -- List of top five predictions and normalized scores as tuple
    """
    top_predictions = []
    normalized_prediction_score = []
    for i in range(1):
        predicted_dec_dup = predicted_decision[i]
        predicted_dec_dup_sorted = sorted(predicted_dec_dup, reverse=True)
        max_s = max(predicted_dec_dup_sorted)
        min_s = min(predicted_dec_dup_sorted)

        normalized_prediction_score = \
            [
                int(float(val - min_s) * 100 / float(max_s - min_s)) for val in predicted_dec_dup_sorted
            ]

        for j in range(len(predicted_dec_dup)):
            top_predictions.append(
                labels_names[predicted_decision[i].tolist().index(predicted_dec_dup_sorted[j])]
            )

    return top_predictions, normalized_prediction_score


@iHire.route('/')
def hello_world():
    return render_template('index_homepage.html')

@iHire.route('/results_home')
def results_home():
    return render_template('index_result.html')

@iHire.route('/results')
def results():
    global results_json
    return json.dumps(results_json)

@iHire.route('/clear_results')
def clear_results():
    global results_json
    results_json = dict()
    return json.dumps(results_json)

@iHire.route('/network')
def network():
    global university
    return render_template('network.html', parameter=university)

@iHire.route('/about')
def about():
    return render_template('about.html')

@iHire.route('/submit', methods=['POST'])
def submit():
    global university
    if request.method == 'POST':
        print "printing value from ajax call"
        if "major" in request.form:
            print "here"
            major = str(request.form["major"])
            major = major.strip('"')
            if "university" in request.form:
                university_ip = str(request.form["university"])
                print university_ip
                university_ip = university_ip.strip('"')
                create_data_for_graph(university_ip, major, skills_employer, univ_major_number, major_code_lookup)
                create_data_for_tree(university_ip, major, skills_employer_tree, univ_major_number, major_code_lookup)
            else:
                create_data_for_graph(university, major, skills_employer, univ_major_number, major_code_lookup)
                create_data_for_tree(university, major, skills_employer_tree, univ_major_number, major_code_lookup)
        return str(request.form["major"])

@iHire.route('/skill_submit', methods=['POST'])
def skill_submit():
    titles = []
    if "skill" in request.form:
        skill = str(request.form["skill"])
        skill = skill.strip('"')
        for title in skills_map_with_percent:
            if skill in skills_map_with_percent[title]["skills"]:
                titles.append(title)
    return json.dumps(titles)

@iHire.route("/analyze", methods=['POST','GET'])
def analyze():
    global flag
    global results_json
    if request.method:
        flag = 1
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
                text_from_pdf = text_from_pdf.replace('\xc2\xa0', ' ')
                with open(filename_without_extension + '.txt', 'wb') as write_file:
                    write_file.write(text_from_pdf)

                textfile_name = filename_without_extension + '.txt'
            else:
                textfile_name = filename

            print filename
            global university
            university = extract_univ(open(textfile_name).read(), univ_dict, univ_normalize)
            print university
            create_data_for_graph(university, "", skills_employer, univ_major_number, major_code_lookup)
            create_data_for_tree(university, "", skills_employer_tree, univ_major_number, major_code_lookup)

            resume_text = [open(textfile_name).read()]
            # resume_tfidf = tfidf_vect.transform(resume_text)
            # predicted_decision = model.decision_function(resume_tfidf)
            predicted_decision = model.decision_function(resume_text)

            top_predictions, normalized_prediction_score = get_top_predictions(predicted_decision)

            out = dict()
            out["university"] = university

            skills_map_with_percent_list = []
            titles = sorted(skills_map_with_percent.keys())
            for title in titles:
                temp_skill_map = dict()
                temp_skill_map[title] = skills_map_with_percent[title]
                skills_map_with_percent_list.append(temp_skill_map)

            out["skills_map"] = skills_map_with_percent_list
            out["titles"] = titles

            out["candidate_skills"] = dict()
            out["title_data"] = dict()

            try:
                tokens = nltk.word_tokenize(resume_text[0].lower())
            except UnicodeDecodeError:
                tokens = nltk.word_tokenize(resume_text[0].decode('utf-8').lower())

            skill_score = []
            for pred in top_predictions:
                try:
                    top15 = skills_map_with_percent[title_title_map[pred]]["skills"][:15]
                except KeyError:
                    top15 = []
                temp_skill_list = [t for t in top15 if len(t) > 1 and t.lower() in tokens]

                out["candidate_skills"][title_title_map[pred]] = temp_skill_list
                out["title_data"][title_title_map[pred]] = titles_data[title_title_map[pred]]
                skill_score.append(int(len(temp_skill_list) / 15.0 * 100.0))

            final_score = [sum(x)/2 for x in zip(normalized_prediction_score, skill_score)]

            final_titles_list = []
            sorted_score_indexes = [i[0] for i in sorted(enumerate(final_score), key=lambda x:x[1], reverse=True)]

            for s in sorted_score_indexes:
                final_titles_list.append(title_title_map[top_predictions[s]])

            final_score_sorted = sorted(final_score, reverse=True)

            # print normalized_prediction_score
            # print final_titles_list
            # print final_score_sorted

            out["final_prediction_list"] = final_titles_list
            out["final_score_sorted"] = final_score_sorted

            if os.path.isfile(textfile_name):
                    os.remove(textfile_name)

            if os.path.isfile(filename):
                    os.remove(filename)

            results_json = OrderedDict(out)
            return json.dumps(OrderedDict(out))
            # return render_template('index_result.html')
    
if __name__ == '__main__':
    iHire.run(host='0.0.0.0')




