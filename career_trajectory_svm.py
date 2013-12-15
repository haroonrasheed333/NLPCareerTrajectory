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

    num_resumes = len(data_dict['label'])

    # Split the data training and test datasets
    train_resumes = data_dict['data'][0:int(num_resumes*0.9)]
    train_labels = data_dict['label'][0:int(num_resumes*0.9)]

    count_vect = CountVectorizer()
    train_counts = vectorize(count_vect, train_resumes)
    tfidf_train = tfidftransform(train_counts)
    clf = trainsvm(tfidf_train, train_labels)

    test_resumes = data_dict['data'][int(num_resumes*0.9) + 1:]
    test_labels = data_dict['label'][int(num_resumes*0.9) + 1:]

    test_counts = count_vect.transform(test_resumes)
    tfidf_test = tfidftransform(test_counts)
    predicted = clf.predict(tfidf_test)

    accuracy = np.mean(predicted == test_labels)
    p = precision_score(test_labels, predicted, average='macro')
    r = recall_score(test_labels, predicted, average='macro')

    print accuracy
    print p
    print r

    print classification_report([t for t in test_labels], [p for p in predicted])