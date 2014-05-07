from __future__ import division
import os
import nltk
import pickle
import random
import numpy as np
from util import ResumeCorpus
from nltk.corpus import stopwords
from sklearn.svm import LinearSVC
from nltk.stem.porter import PorterStemmer
from sklearn.pipeline import FeatureUnion
from sklearn.feature_extraction.text import TfidfTransformer
from marisa_vectorizers import MarisaTfidfVectorizer
from sklearn.metrics import precision_score, recall_score, classification_report


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


def get_degree(resume_text):
    resume_text = resume_text.lower()

    if 'education' in resume_text:
        parted = resume_text.split('education')[1]
        edu_text = parted[:150]
    else:
        edu_text = resume_text
    degree_level = 0

    for d in ["doctor ", "ph.d", "phd", "ph. d"]:
        if d in edu_text:
            return 0.021

    masters = \
        [
            "master", "ms degree", "mpa ", "mhrm", "mfa ", "mba ", "m.sc", "m.s ", "m.h.a", "m.f.a", "m.b.a", "m. s",
            "m.a", "m. tech", "m. ed", "m. a"
        ]

    for m in masters:
        if m in edu_text:
            return 0.018

    bachelors = \
        [
            "bachelor", "bsc", "bsit", "bse", "bsba", "bs of", "bs degree", "bgs", "bfa", "bba", "bs ", "ba ", "b.sc",
            "b.s.n", "b.s.", "b.s. ", "b.phil", "b.f.a", "b.e", "b.com", "b.b.a", "b.a.", "b.tech", "b. tech", "b. a",
            "bs,"
        ]

    for b in bachelors:
        if b in edu_text:
            return 0.016

    associate = ["associate", "as degree", "as ", "aas ", "a.s.", "a.s ", "a.a.s","a.a. ", "a. a"]

    for a in associate:
        if a in edu_text:
            return 0.014

    if "diploma" in edu_text:
        return 0.013

    high_school = ["high school diploma", "hs dip", "h. s. ", "high school degree", "h.s "]

    for h in high_school:
        if h in edu_text:
            return 0.012

    return degree_level


def get_degree_level_from_resume(resume_data):
    degree_level = [get_degree(resume_text) for (resume_text, tag, fname) in resume_data ]
    return degree_level


def get_skill_features(resume_text, top_skills):
    skill_features = []
    tokens = nltk.word_tokenize(resume_text.lower())
    tokens = [st.stem(token) for token in tokens]

    for skill in top_skills:
        if skill in tokens:
            skill_features.append(1)
        else:
            skill_features.append(0)

    return skill_features


def get_skill_features_from_resume(resume_data, top_skills):
    skill_list = [get_skill_features(resume_text, top_skills) for (resume_text, tag, fname) in resume_data ]
    return skill_list


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

    # print "Extract degree level from training resumes"
    # train_degree_level = np.array([get_degree_level_from_resume(train_resumes)])
    #
    # print "Extract degree level from testing resumes"
    # test_degree_level = np.array([get_degree_level_from_resume(test_resumes)])

    # TfidfVectorizer (unigrams + bigrams)
    marisa_uni_vect = MarisaTfidfVectorizer(
        decode_error='ignore',
        stop_words='english',
        ngram_range=(1, 2),
        max_df=0.75,
        max_features=1000
    )
    # marisa_bi_vect = MarisaTfidfVectorizer(
    #     stop_words='english',
    #     ngram_range=(2, 2),
    #     decode_error='ignore'
    # )

    vectorizer = FeatureUnion([('uni', marisa_uni_vect)])
    # vectorizer = FeatureUnion([('uni', marisa_uni_vect), ('bi', marisa_bi_vect)])

    print "Create training resume feature vector"
    train_tfidf = vectorizer.fit_transform(train_resume_text)

    # print "Convert train feature vector to array"
    # train_tfidf_array = train_tfidf.toarray()

    # print "Concatenate degree level to the train featureset"
    # train_tfidf_array_degree_level = np.concatenate((train_tfidf_array, train_degree_level.T), axis=1)
    clf = trainsvm(train_tfidf, train_labels)

    print "Create test resume feature vector"
    test_tfidf = vectorizer.transform(test_resume_text)

    # print "Convert test feature vector to array"
    # test_tfidf_array = test_tfidf.toarray()
    #
    # print "Concatenate degree level to the test featureset"
    # test_tfidf_array_degree_level = np.concatenate((test_tfidf_array, test_degree_level.T), axis=1)

    print "Predict testing labels"
    predicted_score = clf.predict(test_tfidf)
    predicted_decision = clf.decision_function(test_tfidf)

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

    # Pickle the classifier and training features to test it on the heldout dataset.
    with open('svmclassifier_new_0420_marisa.pkl', 'wb') as outfile:
        pickle.dump(clf, outfile)

    with open('label_names_0420_marisa.pkl', 'wb') as lab_names:
        pickle.dump(labels_names, lab_names)

    with open('tfidf_vect_0420_marisa.pkl', 'wb') as hash_v:
        pickle.dump(vectorizer, hash_v)
