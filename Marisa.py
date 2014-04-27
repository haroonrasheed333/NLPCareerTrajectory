from __future__ import division
import os
import pickle
import marisa_trie
from util import ResumeCorpus
from nltk.corpus import stopwords
from sklearn.svm import LinearSVC
from nltk.stem.porter import PorterStemmer
from sklearn.pipeline import FeatureUnion
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, HashingVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from marisa_vectorizers import (
    MarisaCountVectorizer,
    MarisaTfidfVectorizer,
    MarisaCountVectorizerOld,
    ReducedCountVectorizer,
)


st = PorterStemmer()
stopwords = stopwords.words('english')


def trainsvm(featureset, train_label):
    clf = LinearSVC().fit(featureset, train_label)
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
    train_resumes = traintest_corpus.resumes[0:int(num_resumes*0.9)]
    test_resumes = traintest_corpus.resumes[int(num_resumes*0.9) + 1:]
    #
    # train_resumes = traintest_corpus.resumes[0:200]
    # test_resumes = traintest_corpus.resumes[200:220]

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

    # CountVectorizer + TfidfTransformer
    # count_vect = CountVectorizer(stop_words='english')
    # print "Create training resume counts"
    # train_counts = vectorize(count_vect, train_resume_text)
    # print "Create tfidf vector for training featureset"
    # tfidf_train = tfidftransform(train_counts)
    # clf = trainsvm(tfidf_train, train_labels)
    #
    # print "Create testing resume counts"
    # test_counts = count_vect.transform(test_resume_text)
    # print "Create tfidf vector for testing featureset"
    # tfidf_test = tfidftransform(test_counts)

    # TfidfVectorizer
    # tfidf_vect = TfidfVectorizer(stop_words='english')
    # print "Create training resume tfidf"
    # train_tfidf = tfidf_vect.fit_transform(train_resume_text)
    # clf = trainsvm(train_tfidf, train_labels)
    #
    # print "Create testing resume counts"
    # test_tfidf = tfidf_vect.transform(test_resume_text)
    #
    # # predicted = clf.predict(test_featureset)
    # print "Predict testing labels"
    # predicted = clf.predict(test_tfidf)
    # # predicted_decision = clf.decision_function(test_featureset)
    # predicted_decision = clf.decision_function(test_tfidf)

    # HashingVectorizer
    # hash_vect = HashingVectorizer(stop_words='english')
    # print "Create training resume hash"
    # train_hash = hash_vect.transform(train_resume_text)
    # clf = trainsvm(train_hash, train_labels)
    #
    # print "Create testing resume hash"
    # test_hash = hash_vect.transform(test_resume_text)
    #
    # # predicted = clf.predict(test_featureset)
    # print "Predict testing labels"
    # predicted = clf.predict(test_hash)
    # # predicted_decision = clf.decision_function(test_featureset)
    # predicted_decision = clf.decision_function(test_hash)

    # CountVectorizer
    # count_vect = CountVectorizer(stop_words='english')
    # print "Create training resume counts"
    # train_counts = count_vect.fit_transform(train_resume_text)
    # clf = trainsvm(train_counts, train_labels)
    #
    # print "Create testing resume counts"
    # test_counts = count_vect.transform(test_resume_text)
    #
    # # predicted = clf.predict(test_featureset)
    # print "Predict testing labels"
    # predicted = clf.predict(test_counts)
    # # predicted_decision = clf.decision_function(test_featureset)
    # predicted_decision = clf.decision_function(test_counts)

    # TfidfVectorizer (unigrams + bigrams)
    marisa_uni_vect = MarisaTfidfVectorizer(
        decode_error='ignore',
        stop_words='english',
        ngram_range=(1, 1),
        max_features=10000
    )
    # marisa_bi_vect = MarisaTfidfVectorizer(
    #     stop_words='english',
    #     ngram_range=(2, 2),
    #     decode_error='ignore',
    #     max_features=2000
    # )

    vectorizer = FeatureUnion([('uni', marisa_uni_vect)])

    print "Create training resume hash"
    train_hash = vectorizer.fit_transform(train_resume_text)
    clf = trainsvm(train_hash, train_labels)

    print "Create testing resume hash"
    test_hash = vectorizer.transform(test_resume_text)

    print "Predict testing labels"
    predicted_score = clf.predict(test_hash)
    predicted_decision = clf.decision_function(test_hash)

    #accuracy = np.mean(predicted == test_labels)
    #p = precision_score(test_labels, predicted, average='macro')
    #r = recall_score(test_labels, predicted, average='macro')
    #
    #print accuracy
    #print p
    #print r
    #
    #print classification_report([t for t in test_labels], [p for p in predicted])
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

    with open('hash_vect_0420_marisa.pkl', 'wb') as hash_v:
        pickle.dump(vectorizer, hash_v)