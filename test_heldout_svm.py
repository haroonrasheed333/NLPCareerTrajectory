from __future__ import division
import os
import random
import pickle
from nltk import bigrams
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from career_trajectory_svm import tfidftransform
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.svm import LinearSVC, libsvm
from sklearn.metrics import precision_score, recall_score, classification_report
from collections import defaultdict

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
            self.labels_file = self.source_dir + '/labels_heldout_0408.txt'
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
                resume_tag = filename_tag[1].rstrip()
                resumes.append((open(self.source_dir + '/heldout_0408/' + filename).read(), resume_tag, filename))
            except IOError, (ErrorNumber, ErrorMessage):
                if ErrorNumber == 2:
                    pass

        return resumes


def pre_processing(resume):
    """
    Function to create unigrams and remove stopwords from the data.

    Args:
        resume -- text of the resume as string.

    Returns:
        vocab - list of stemmed unigrams and bigrams from the resume string.
    """
    unigrams = resume.lower().split()
    vocab = [st.stem(word) for word in unigrams if word not in stopwords]

    bigrms = bigrams(unigrams)
    bigrams_list = []
    bigrams_list += [bigr[0] + bigr[1] for bigr in bigrms if (bigr[0] not in stopwords and bigr[1] not in stopwords)]

    return vocab + bigrams_list


def prepare_data():
    """
    Function to prepare the data. Read the source files and extract the text and label for each resume.
    """
    user_name = os.environ.get('USER')
    traintest_corpus = ResumeCorpus('/Users/' + user_name + '/Documents/Data')
    random.shuffle(traintest_corpus.resumes)

    for resume in traintest_corpus.resumes:
        try:
            review_text = pre_processing(resume[0])
            review_text = " ".join(review_text)
            data_dict['data'].append(review_text)
            data_dict['label'].append(resume[1])
        except:
            pass


def main():
    """
    Test the heldout dataset using the trained classifier and features
    """
    prepare_data()

    # Get the pickled classifier model and features
    with open('svmclassifier.pkl', 'rb') as infile:
        model = pickle.load(infile)

    with open('label_names.pkl', 'rb') as lab_names:
        labels_names = pickle.load(lab_names)

    with open('count_vect.pkl', 'rb') as count_v:
        count_vect = pickle.load(count_v)

    test_resumes = data_dict['data'][:]
    test_labels = data_dict['label'][:]

    test_counts = count_vect.transform(test_resumes)
    tfidf_test = tfidftransform(test_counts)
    predicted_score = model.predict(tfidf_test)
    predicted_decision = model.decision_function(tfidf_test)

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

    print "New Accuracy (Label present in one of the 5 predictions): " + str(sum(accuracy_list_top_5) / len(accuracy_list_top_5))


if __name__ == '__main__':
    main()