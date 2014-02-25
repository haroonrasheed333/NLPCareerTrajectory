from __future__ import division
import os
import random
import numpy as np
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.svm import LinearSVC
from career_trajectory import ResumeCorpus
from sklearn.metrics import precision_score, recall_score, classification_report
from collections import defaultdict

st = PorterStemmer()
stopwords = stopwords.words('english')
data_dict = defaultdict(list)


def pre_processing(resume):
    """
    Function to create unigrams and remove stopwords from the data.

    Args:
        resume -- text of the resume as string.

    Returns:
        vocab - list of stemmed unigrams from the resume string.
    """
    unigrams = resume.split()
    word_list = [word.lower() for word in unigrams if word.lower() not in stopwords]
    word_list = [st.stem(word) for word in word_list if word]
    vocab = [word for word in word_list if word not in stopwords]
    return vocab


def prepare_data():
    """
    Function to prepare the data. Read the source files and extract the text and label for each resume.
    """
    user_name = os.environ.get('USER')
    traintest_corpus = ResumeCorpus('/Users/' + user_name + '/Documents/Data')
    random.shuffle(traintest_corpus.resumes)
    #label_dict = {'Administrative Assistant': 0, 'Assistant Manager': 1, 'Business Analyst': 2, 'Consultant': 3,
    #              'Customer Service Representative': 4, 'Director': 5, 'Graphic Designer': 6, 'Intern': 7,
    #              'Manager': 8, 'Marketing Manager': 9, 'President': 10, 'Project Manager': 11, 'Research Assistant': 12,
    #              'Sales Associate': 13, 'Senior Manager': 14, 'Senior Software Engineer': 15, 'Software Engineer': 16,
    #              'Vice President': 17, 'Web Developer': 18}
    for resume in traintest_corpus.resumes:
        try:
            review_text = pre_processing(resume[0])
            review_text = " ".join(review_text)
            data_dict['data'].append(review_text)
            data_dict['label'].append(resume[1])
        except:
            pass


def vectorize(count_vect, data):
    x_counts = count_vect.fit_transform(data)
    return x_counts


def tfidftransform(counts):
    tfidf_transformer = TfidfTransformer()
    x_tfidf = tfidf_transformer.fit_transform(counts)
    return x_tfidf


def trainnb(tfidf, train_label):
    clf = MultinomialNB().fit(tfidf, train_label)
    return clf


def trainsvm(tfidf, train_label):
    clf = LinearSVC().fit(tfidf, train_label)
    return clf



if __name__ == '__main__':
    # Prepare data
    prepare_data()

    #label_dict1 = {0: 'Administrative Assistant', 1: 'Assistant Manager', 2: 'Business Analyst', 3: 'Consultant',
    #              4: 'Customer Service Representative', 5: 'Director', 6: 'Graphic Designer', 7: 'Intern',
    #              8: 'Manager', 9: 'Marketing Manager', 10: 'President', 11: 'Project Manager', 12: 'Research Assistant',
    #              13: 'Sales Associate', 14: 'Senior Manager', 15: 'Senior Software Engineer', 16: 'Software Engineer',
    #              17: 'Vice President', 18: 'Web Developer'}

    num_resumes = len(data_dict['label'])

    # Split the data training and test datasets
    train_resumes = data_dict['data'][0:int(num_resumes*0.9)]
    train_labels = data_dict['label'][0:int(num_resumes*0.9)]

    labels_names = sorted(list(set(train_labels)))

    count_vect = CountVectorizer()
    train_counts = vectorize(count_vect, train_resumes)
    tfidf_train = tfidftransform(train_counts)
    clf = trainnb(tfidf_train, train_labels)

    test_resumes = data_dict['data'][int(num_resumes*0.9) + 1:]
    test_labels = data_dict['label'][int(num_resumes*0.9) + 1:]

    test_counts = count_vect.transform(test_resumes)
    tfidf_test = tfidftransform(test_counts)
    predicted = clf.predict(tfidf_test)
    predicted_prob = clf.predict_proba(tfidf_test)

    #accuracy = np.mean(predicted == test_labels)
    #p = precision_score(test_labels, predicted, average='macro')
    #r = recall_score(test_labels, predicted, average='macro')
    #
    #print accuracy
    #print p
    #print r
    #
    #print classification_report([t for t in test_labels], [p for p in predicted])

    actual_vs_predicted = []
    predicted = []

    for i in range(len(test_labels)):
        actual_label = test_labels[i]
        predicted_prob_dup = predicted_prob[i]
        predicted_prob_dup_sorted = sorted(predicted_prob_dup, reverse=True)
        top_five_predictions = []
        predicted.append(labels_names[predicted_prob[i].tolist().index(predicted_prob_dup_sorted[0])])
        for j in range(5):
            top_five_predictions.append(labels_names[predicted_prob[i].tolist().index(predicted_prob_dup_sorted[j])])

        actual_vs_predicted.append([actual_label, top_five_predictions])

    n = 0
    for l in actual_vs_predicted:
        print "\nActual: " + l[0]
        print "Predicted: " + predicted[n]
        print "Predicted: " + ", ".join(l[1])
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
