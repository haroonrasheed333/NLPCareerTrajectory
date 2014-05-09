from __future__ import division
import os
import pickle
import numpy as np
from nltk.corpus import stopwords
from collections import defaultdict
from nltk.stem.porter import PorterStemmer
from sklearn.metrics import precision_score, recall_score, classification_report

st = PorterStemmer()
stopwords = stopwords.words('english')
data_dict = defaultdict(list)
user_name = os.environ.get('USER')


class ResumeCorpus():
    """
    Class to read the source files from source directory and create a
    list of tuples with resume_text, tag and filename for each resume.

    Parameters:
    -----------
    source_dir -- string.
        The path of the source directory.

    labels_file -- string.
        The path of the labels file (default: None)

    """

    def __init__(self, source_dir, labels_file=None):
        self.source_dir = source_dir
        if not labels_file:
            self.labels_file = self.source_dir + '/labels_heldout_0426.txt'
        else:
            self.labels_file = labels_file
        self.resumes = self.read_files()

    def read_files(self):
        """
        Method to return a list of tuples with resume_text, tag and filename for the training data

        Parameters:
        -----------
        No Argument

        Returns:
        --------
        resumes -- list
            List of tuples with resume_text, tag and filename for the training data

        """
        resumes = []

        for line in open(self.labels_file).readlines():
            try:
                filename_tag = line.split('\t')
                filename = filename_tag[0]
                resume_tag = filename_tag[1].rstrip()
                resumes.append((open(self.source_dir + '/heldout_0426/' + filename).read(), resume_tag, filename))
            except IOError, (ErrorNumber, ErrorMessage):
                if ErrorNumber == 2:
                    pass

        return resumes


def main():
    """
    Test the heldout dataset using the trained classifier and features
    """

    # Read Heldout corpus
    heldout_corpus = ResumeCorpus('/Users/' + user_name + '/Documents/Data')

    # Get the pickled classifier model and features
    with open('iBeyond_classifier.pkl', 'rb') as infile:
        model = pickle.load(infile)

    with open('iBeyond_labels.pkl', 'rb') as lab_names:
        labels_names = pickle.load(lab_names)

    heldout_resumes = heldout_corpus.resumes

    heldout_labels = []
    heldout_resume_text = []

    # Extract heldout resume text
    for (text, label, fname) in heldout_resumes:
        heldout_labels.append(label)
        heldout_resume_text.append(text)

    # Predict classes for heldout data
    predicted_labels = model.predict(heldout_resume_text)
    predicted_decision = model.decision_function(heldout_resume_text)

    accuracy = np.mean(predicted_labels == heldout_labels)
    precision = precision_score(heldout_labels, predicted_labels, average='weighted')
    recall = recall_score(heldout_labels, predicted_labels, average='weighted')

    print accuracy
    print precision
    print recall

    print classification_report([t for t in heldout_labels], [p for p in predicted_labels])

    # predicted = []
    #
    # actual_vs_predicted = []
    #
    # for i in range(len(heldout_labels)):
    #     actual_label = heldout_labels[i]
    #     predicted_dec_dup = predicted_decision[i]
    #     predicted_dec_dup_sorted = sorted(predicted_dec_dup, reverse=True)
    #     top_five_predictions = []
    #     predicted.append(labels_names[predicted_decision[i].tolist().index(predicted_dec_dup_sorted[0])])
    #     for j in range(5):
    #         top_five_predictions.append(labels_names[predicted_decision[i].tolist().index(predicted_dec_dup_sorted[j])])
    #
    #     actual_vs_predicted.append([actual_label, top_five_predictions])
    #
    # n = 0
    # for l in actual_vs_predicted:
    #     print "\nActual: " + l[0]
    #     print "Predicted: " + predicted[n]
    #     print "Predicted top5: " + ", ".join(l[1])
    #     n += 1
    #
    # accuracy_list = []
    # accuracy_list_top_5 = []
    #
    # for i in range(len(heldout_labels)):
    #     accuracy_list.append(0)
    #     accuracy_list_top_5.append(0)
    #
    # for j in range(len(heldout_labels)):
    #     if actual_vs_predicted[j][0] in actual_vs_predicted[j][1]:
    #         accuracy_list_top_5[j] = 1
    #
    #     if predicted[j] == heldout_labels[j]:
    #         accuracy_list[j] = 1
    #
    # print "Actual Accuracy: " + str(sum(accuracy_list) / len(accuracy_list))
    #
    # print "New Accuracy (Label present in one of the 5 predictions): " +
    # str(sum(accuracy_list_top_5) / len(accuracy_list_top_5))


if __name__ == '__main__':
    main()