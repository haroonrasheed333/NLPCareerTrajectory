from __future__ import division
import os
import nltk
import pickle
import random
import numpy as np
from util import ResumeCorpus
from nltk.corpus import stopwords
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from nltk.stem.porter import PorterStemmer
from sklearn.pipeline import FeatureUnion
from sklearn.grid_search import GridSearchCV
from marisa_vectorizers import MarisaTfidfVectorizer
from sklearn.cross_validation import train_test_split
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics import precision_score, recall_score, classification_report
from util2 import get_degree, get_degree_level_from_resume

from pprint import pprint
from time import time
import logging

user_name = os.environ.get('USER')
st = PorterStemmer()
stopwords = stopwords.words('english')


def get_accuracy(predicted_labels_list, test_labels_list):
    """
    Function to calculate the mean prediction accuracy

    Parameters:
    -----------
    predicted_labels -- list
        List of labels predicted by the classifier for each test data

    test_labels -- list
        List of actual labels for each of the test data

    Returns:
    --------
    mean -- float
        Mean accuracy of the prediction
    """
    mean = np.mean(predicted_labels_list == test_labels_list)
    return mean


def get_actual_vs_predicted(predicted_decision, test_labels, labels_names):
    """
    Function to calculate the mean prediction accuracy

    Parameters:
    -----------
    predicted_decision -- numpy array
        Decision scores for each (test_data, class) combination.
        The array has shape (num_samples, num_classes)

    test_labels -- list
        List of actual labels for each of the test data

    Returns:
    --------
    actual_vs_predicted -- list
        Actual vs Top five predicted labels for each each test data
    """
    actual_vs_predicted_list = []
    for i in range(len(test_labels)):
        actual_label = test_labels[i]
        predicted_dec_dup = predicted_decision[i]
        predicted_dec_dup_sorted = sorted(predicted_dec_dup, reverse=True)
        top_five_predictions = []
        for j in range(5):
            top_five_predictions.append(labels_names[predicted_decision[i].tolist().index(predicted_dec_dup_sorted[j])])

        actual_vs_predicted_list.append([actual_label, top_five_predictions])

    return actual_vs_predicted_list


def get_best_estimator_parameters(corpus_data_text, corpus_data_labels):
    """
    Function to estimate the best parameters to use for the vectorizer and classifier

    Parameters:
    -----------
    corpus_data_text -- list
        List of corpus data

    corpus_data_labels -- list
        List of class labels.
    """

    # Create a Pipeline
    print "Create pipeline for vectorizer => classifier"
    vect_clf_pipeline = Pipeline([('vect', MarisaTfidfVectorizer()),
                         ('clf', LinearSVC())])

    parameters = {
        'vect__max_df': (0.5, 0.75, 1.0),
        'vect__max_features': (None, 5000, 10000, 25000, 50000, 75000, 100000),
        'vect__stop_words': (None, 'english'),
        'vect__ngram_range': ((1, 1), (1, 2)),  # unigrams or bigrams
        # 'vect__use_idf': (True, False),
        # 'vect__norm': ('l1', 'l2'),
        #'clf__n_iter': (10, 50, 80),
    }

    grid_search = GridSearchCV(vect_clf_pipeline, parameters, verbose=2, n_jobs=-1)

    print("Performing grid search...")
    print("pipeline:", [name for name, _ in vect_clf_pipeline.steps])
    print("parameters:")
    pprint(parameters)
    t0 = time()
    grid_search.fit(corpus_data_text, corpus_data_labels)
    print("done in %0.3fs" % (time() - t0))
    print()

    print("Best score: %0.3f" % grid_search.best_score_)
    print("Best parameters set:")
    best_parameters = grid_search.best_estimator_.get_params()
    for param_name in sorted(parameters.keys()):
        print("\t%s: %r" % (param_name, best_parameters[param_name]))


def create_pipeline():
    """
    Function to build a pipeline of vectorizer / classifier steps.


    Parameters:
    -----------
    None

    Returns:
    --------
    vect_clf_pipeline -- pipeline object
        A pipeline object consisting of vectorizer / classifier steps.
    """

    # Create a Vectorizer using the best parameters returned by GridSearchCV
    vectorizer = MarisaTfidfVectorizer(
        decode_error='ignore',
        stop_words='english',
        ngram_range=(1, 2),
        max_df=0.75,
        max_features=100000
    )
    vect_clf_pipeline = Pipeline([('vect', vectorizer),
                                  ('clf', LinearSVC())])

    return vect_clf_pipeline


def display_results(actual_vs_predicted_list):
    """
    Function to display the classification results tested on the test data

    Parameters:
    -----------
    actual_vs_predicted -- list
        Actual vs Top five predicted labels for each each test data
    """

    for l in actual_vs_predicted_list:
        print "\nActual: " + l[0]
        print "Predicted: " + l[1][0]
        print "Predicted top5: " + ", ".join(l[1])


def get_new_accuracy(actual_vs_predicted_list, test_labels):
    """
    Function to calculate the new prediction accuracy considering top 5 predictions for each test data

    Parameters:
    -----------
    actual_vs_predicted -- list
        Actual vs Top five predicted labels for each each test data

    test_labels -- list
        List of actual labels for each of the test data

    Returns:
    --------
    acc -- float
        Prediction accuracy considering top 5 predictions for each test data
    """

    accuracy_list_top_5 = []
    for i in range(len(test_labels)):
        accuracy_list_top_5.append(0)

    for j in range(len(test_labels)):
        if actual_vs_predicted_list[j][0] in actual_vs_predicted_list[j][1]:
            accuracy_list_top_5[j] = 1

    acc = sum(accuracy_list_top_5) / len(accuracy_list_top_5)
    return acc


def ibeyond_classifier():
    traintest_corpus = ResumeCorpus('/Users/' + user_name + '/Documents/Data')

    # Shuffle the corpus
    # print "Shuffle the corpus"
    random.seed()
    random.shuffle(traintest_corpus.resumes)

    corpus_text = []
    corpus_labels = []

    for (text, label, fname) in traintest_corpus.resumes:
        corpus_labels.append(label)
        corpus_text.append(text)

    # Split training and testing data
    train_text, test_text, train_labels, test_labels = train_test_split(corpus_text, corpus_labels, test_size=0.20)

    labels_names = sorted(list(set(train_labels)))

    # get_best_estimator_parameters(corpus_text, corpus_labels)

    # Create pipeline for vectorizer => classifier
    vect_clf = create_pipeline()

    # Train Model
    vect_clf = vect_clf.fit(train_text, train_labels)

    # Predict test samples
    predicted_labels = vect_clf.predict(test_text)
    predicted_decision = vect_clf.decision_function(test_text)

    # Calculate accuracy, precision, and recall scores
    accuracy = get_accuracy(predicted_labels, test_labels)
    precision = precision_score(test_labels, predicted_labels, average='weighted')
    recall = recall_score(test_labels, predicted_labels, average='weighted')
    report = classification_report([t for t in test_labels], [p for p in predicted_labels])

    # Get Actual vs. Top 5 predicted results for each test data
    actual_vs_predicted = get_actual_vs_predicted(predicted_decision, test_labels, labels_names)

    # Display classification results
    display_results(actual_vs_predicted)

    # Compute new accuracy
    new_accuracy = get_new_accuracy(actual_vs_predicted, test_labels)

    print "Accuracy: " + str(accuracy)
    print "Precision: " + str(precision)
    print "Recall: " + str(recall)
    print "New Accuracy (Label present in one of the 5 predictions): " + str(new_accuracy)

    # # Pickle the classifier and training features to test it on the heldout dataset.
    # print "Pickle classifier"
    # with open('iBeyond_classifier.pkl', 'wb') as outfile:
    #     pickle.dump(vect_clf, outfile)
    #
    # with open('iBeyond_labels.pkl', 'wb') as lab_names:
    #     pickle.dump(labels_names, lab_names)
    #
    # # with open('tfidf_vect_0420_marisa.pkl', 'wb') as hash_v:
    # #     pickle.dump(vectorizer, hash_v)


if __name__ == '__main__':
    ibeyond_classifier()