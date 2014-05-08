from __future__ import division
import re
import os
import json
import nltk
import random
import pickle
from lxml import etree
from nltk import bigrams
from nltk import FreqDist
from collections import Counter
from nltk.corpus import stopwords
from sklearn.svm import LinearSVC
from collections import defaultdict
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from univ_lookup import extract_univ

univ_dict = json.loads(open("static/univs_list.json","rb").read())
univ_normalize = json.loads(open("static/univ_map.json","rb").read())

st = PorterStemmer()
stopwords = stopwords.words('english')
data_dict = defaultdict(list)


class ResumeCorpus():
    """
    Class to read the source files from source directory and create a list of tuples with resume_text, tag and filename
    for each resume.

    Args:
        source_dir -- string. The path of the source directory.
        labels_file -- string. The path of the labels file (default: None)
    """
    def __init__(self, source_dir, labels_file=None):

        self.source_dir = source_dir
        if not labels_file:
            self.labels_file = self.source_dir + '/labels_0426.txt'
        else:
            self.labels_file = labels_file
        self.resumes = self.read_files()

    def read_files(self):
        """
        Method to return a list of tuples with resume_text, tag and filename for the training data

        Args:
            No Argument

        Returns:
            resumes -- list of tuples with resume_text, tag and filename for the training data
        """
        resumes = []

        for line in open(self.labels_file).readlines():
            try:
                filename_tag = line.split('\t')
                filename = filename_tag[0]
                xml_filename = filename.split('_')[0] + '.txt'
                resume_tag = filename_tag[1].rstrip()
                resume_text = open(self.source_dir + '/training_0426/' + filename).read()
                resume_xml_text = open(self.source_dir + '/samples_0426/' + xml_filename).read()
                resumes.append((resume_text, resume_xml_text, resume_tag, filename))
            except IOError, (ErrorNumber, ErrorMessage):
                if ErrorNumber == 2:
                    pass

        return resumes


def read_skills_from_json_file(training_data):
    """
    This function will read from the skills json file, extract the skills that are part of the training data and create
    a dictionary with Job Titles as keys and list of all the skills for that Job Title as values

    Args:
        training_data -- list of tuples. Eg. [(resume, tag, filename), (resume, tag, filename)...]

    Returns:
        skills_dict -- A dictionary with Job Titles as keys and list of all the skills for that Job Title as values
    """

    skills_dict = dict()
    temp_dict = json.loads(open("skills_0426.json").read())
    training_files = [file_name for (resume, resume_xml, resume_label, file_name) in training_data]

    for title in temp_dict:
        for file_name in temp_dict[title]:
            if file_name.keys()[0] in training_files:
                value = skills_dict.get(title.lower(), None)
                if value is not None:
                    skills_dict[title.lower()] = value + file_name[file_name.keys()[0]]
                else:
                    skills_dict[title.lower()] = []
                    skills_dict[title.lower()] = file_name[file_name.keys()[0]]

    return skills_dict


def extract_top_skills(training_data):
    """
    Extract Top Skills for each Job Title from the training dataset.

    Args:
        training_data -- list of tuples. Eg. [(resume, tag, filename), (resume, tag, filename)...]

    Returns:
        A consolidated list of top skills for all the Job Titles

    """
    skills_dict = read_skills_from_json_file(training_data)

    # Read the top n skills for each Job TiTle
    skill_features = []
    for skill in skills_dict:
        skill_list = skills_dict[skill]
        skill_count = Counter(skill_list)
        top_job_skills = sorted(skill_count, key=skill_count.get, reverse=True)[:300]
        skill_features += top_job_skills

    top_job_skills = list(set(skill_features))
    return top_job_skills


def trainsvm(featureset, train_label):
    clf_svm = LinearSVC().fit(featureset, train_label)
    return clf_svm


def vectorize(count_vect, data):
    x_counts = count_vect.fit_transform(data)
    return x_counts


def extract_features(res_text, xml_text):
    xml_tree = etree.fromstring(xml_text)
    words = [st.stem(w) for w in nltk.word_tokenize(res_text.lower()) if w not in stopwords and len(w) > 2]
    features = Counter(words)
    # features = {}
    # words_set = list(set(words))
    # for w in words_set:
    #     features[w] = 1

    university = xml_tree.xpath('//institution/text()')
    if university:
        normalized_univ = extract_univ(university[0], univ_dict, univ_normalize)
        features['university'] = normalized_univ if normalized_univ else university[0]

    degree_level = xml_tree.xpath('//degree/@level')
    if degree_level:
        features['degree_level'] = max(degree_level)

    return features


def feature_extraction_and_consolidation(resumes):

    res_features = [extract_features(res_txt, xml_txt) for (res_txt, xml_txt, res_label, file_name) in resumes]
    return res_features


if __name__ == '__main__':
    user_name = os.environ.get('USER')
    traintest_corpus = ResumeCorpus('/Users/' + user_name + '/Documents/Data')

    # Shuffle the corpus
    # random.seed()
    # random.shuffle(traintest_corpus.resumes)

    # Use 90% of the shuffled corpus as training and remaining 10% as testing datasets
    num_resumes = len(traintest_corpus.resumes)

    # Split the data training and test datasets
    print "Randomly select training and testing samples"
    train_resumes = traintest_corpus.resumes[0:int(num_resumes * 0.8)]
    test_resumes = traintest_corpus.resumes[int(num_resumes * 0.8) + 1:]

    # train_resumes = traintest_corpus.resumes[0:200]
    # test_resumes = traintest_corpus.resumes[200:220]

    train_labels = []
    for (text, xml, label, fname) in train_resumes:
        train_labels.append(label)

    test_labels = []
    for (text, xml, label, fname) in test_resumes:
        test_labels.append(label)

    labels_names = sorted(list(set(train_labels)))

    # Extract the top skills from the training data
    print "Extract top skills"
    # top_skills = extract_top_skills(train_resumes)

    print "Create training featureset"
    train_featureset = feature_extraction_and_consolidation(train_resumes)

    vec = DictVectorizer()
    train_dict = vec.fit_transform(train_featureset)
    clf = trainsvm(train_dict, train_labels)

    test_featureset = feature_extraction_and_consolidation(test_resumes)
    test_dict = vec.transform(test_featureset)
    predicted = clf.predict(test_dict)
    predicted_decision = clf.decision_function(test_dict)

    predicted = []

    actual_vs_predicted = []

    for i in range(len(test_labels)):
        actual_label = test_labels[i]
        predicted_dec_dup = predicted_decision[i]
        predicted_dec_dup_sorted = sorted(predicted_dec_dup, reverse=True)
        top_five_predictions = []
        predicted.append(labels_names[predicted_decision[i].tolist().index(predicted_dec_dup_sorted[0])])
        for j in range(5):
            top_five_predictions.append(labels_names[predicted_decision[i].tolist().index(predicted_dec_dup_sorted[j])])

        actual_vs_predicted.append([actual_label, top_five_predictions])

    n = 0
    for l in actual_vs_predicted:
        print "\nActual: " + l[0]
        print "Predicted: " + predicted[n]
        print "Predicted top5: " + ", ".join(l[1])
        n += 1

    accuracy_list = []
    accuracy_list_top_5 = []

    for i in range(len(test_labels)):
        accuracy_list.append(0)
        accuracy_list_top_5.append(0)

    for j in range(len(test_labels)):
        if actual_vs_predicted[j][0] in actual_vs_predicted[j][1]:
            accuracy_list_top_5[j] = 1

        if predicted[j] == test_labels[j]:
            accuracy_list[j] = 1

    print "Actual Accuracy: " + str(sum(accuracy_list) / len(accuracy_list))

    print "New Accuracy (Label present in one of the 5 predictions): " + \
          str(sum(accuracy_list_top_5) / len(accuracy_list_top_5))

    # Pickle the classifier and training features to test it on the heldout dataset.
    # with open('svmclassifier_new_0418_h_new.pkl', 'wb') as outfile:
    #     pickle.dump(clf, outfile)
    #
    # features = dict()
    # features['top_unigrams'] = top_unigrams
    # features['top_bigrams'] = top_bigrams
    #
    # with open('features_0418_h_new.pkl', 'wb') as f:
    #     pickle.dump(features, f)
    #
    # with open('label_names_0418_h_new.pkl', 'wb') as lab_names:
    #     pickle.dump(labels_names, lab_names)
    #
    # with open('count_vect_0418_h_new.pkl', 'wb') as count_v:
    #     pickle.dump(count_vect, count_v)