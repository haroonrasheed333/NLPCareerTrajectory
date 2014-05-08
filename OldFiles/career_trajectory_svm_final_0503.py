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
from sklearn.linear_model import SGDClassifier
from marisa_vectorizers import MarisaTfidfVectorizer
from sklearn.cross_validation import train_test_split
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics import precision_score, recall_score, classification_report
from util2 import get_degree, get_degree_level_from_resume

from pprint import pprint
from time import time
import logging


st = PorterStemmer()
stopwords = stopwords.words('english')


def trainsvm(featureset, train_label):
    clf = LinearSVC(C=1.0, penalty="l2", dual=True).fit(featureset, train_label)
    return clf


def vectorize(count_vect, data):
    x_counts = count_vect.fit_transform(data)
    return x_counts


def tfidftransform(counts):
    tfidf_transformer = TfidfTransformer()
    x_tfidf = tfidf_transformer.fit_transform(counts)
    return x_tfidf


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
    train_resumes = traintest_corpus.resumes[0:int(num_resumes*0.8)]
    test_resumes = traintest_corpus.resumes[int(num_resumes*0.8) + 1:]
    #
    # train_resumes = traintest_corpus.resumes[0:10]
    # test_resumes = traintest_corpus.resumes[10:12]

    train_labels = []
    train_resume_text = []
    for (text, label, fname) in train_resumes:
        train_labels.append(label)
        train_resume_text.append(text)

    test_labels = []
    test_resume_text = []
    for (text, label, fname) in test_resumes:
        test_labels.append(label)
        test_resume_text.append(text)

    labels_names = sorted(list(set(train_labels)))

    # # Create a Pipeline
    # print "Create pipeline for vectorizer => classifier"
    # vect_clf = Pipeline([('vect', MarisaTfidfVectorizer()),
    #                      ('clf', LinearSVC())])
    #
    # parameters = {
    #     'vect__max_df': (0.5, 0.75, 1.0),
    #     'vect__max_features': (None, 5000, 10000, 25000, 50000, 75000, 100000),
    #     'vect__stop_words': (None, 'english'),
    #     'vect__ngram_range': ((1, 1), (1, 2)),  # unigrams or bigrams
    #     # 'vect__use_idf': (True, False),
    #     # 'vect__norm': ('l1', 'l2'),
    #     #'clf__n_iter': (10, 50, 80),
    # }
    #
    # grid_search = GridSearchCV(vect_clf, parameters, verbose=2, n_jobs=-1)
    #
    # print("Performing grid search...")
    # print("pipeline:", [name for name, _ in vect_clf.steps])
    # print("parameters:")
    # pprint(parameters)
    # t0 = time()
    # grid_search.fit(test_resume_text, test_labels)
    # print("done in %0.3fs" % (time() - t0))
    # print()
    #
    # print("Best score: %0.3f" % grid_search.best_score_)
    # print("Best parameters set:")
    # best_parameters = grid_search.best_estimator_.get_params()
    # for param_name in sorted(parameters.keys()):
    #     print("\t%s: %r" % (param_name, best_parameters[param_name]))

    # TfidfVectorizer (unigrams + bigrams)
    marisa_uni_vect = MarisaTfidfVectorizer(
        decode_error='ignore',
        stop_words='english',
        ngram_range=(1, 2),
        max_df=1.0,
        max_features=100000
    )

    print "Create pipeline for vectorizer => classifier"
    vect_clf = Pipeline([('vect', marisa_uni_vect),
                         ('clf', LinearSVC())])

    print "Train Model"
    vect_clf = vect_clf.fit(train_resume_text, train_labels)

    print "Predict test samples"
    predicted_score = vect_clf.predict(test_resume_text)
    predicted_decision = vect_clf.decision_function(test_resume_text)

    # accuracy = np.mean(predicted_score == test_labels)
    # p = precision_score(test_labels, predicted_score, average='macro')
    # r = recall_score(test_labels, predicted_score, average='macro')
    #
    # print accuracy
    # print p
    # print r

    # print classification_report([t for t in test_labels], [p for p in predicted_score])
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

    # # Pickle the classifier and training features to test it on the heldout dataset.
    # with open('svmclassifier_new_0504_marisa.pkl', 'wb') as outfile:
    #     pickle.dump(vect_clf, outfile)
    #
    # with open('label_names_0420_marisa.pkl', 'wb') as lab_names:
    #     pickle.dump(labels_names, lab_names)
    #
    # # with open('tfidf_vect_0420_marisa.pkl', 'wb') as hash_v:
    # #     pickle.dump(vectorizer, hash_v)
