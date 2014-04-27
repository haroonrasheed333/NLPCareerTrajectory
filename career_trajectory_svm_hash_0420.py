from __future__ import division
import re
import os
import json
import nltk
import random
import pickle
from nltk import bigrams
from nltk import FreqDist
from util import ResumeCorpus
from collections import Counter
from nltk.corpus import stopwords
from sklearn.svm import LinearSVC
from collections import defaultdict
from nltk.stem.porter import PorterStemmer
from sklearn.pipeline import FeatureUnion
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, HashingVectorizer
from sklearn.feature_extraction.text import TfidfTransformer


st = PorterStemmer()
stopwords = stopwords.words('english')
data_dict = defaultdict(list)


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
    temp_dict = json.loads(open("skills_0418_no_stemming.json").read())
    training_files = [fname for (resume, resume_label, fname) in training_data]

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
        top_job_skills = sorted(skill_count, key=skill_count.get, reverse=True)[:]
        skill_features += top_job_skills

    top_job_skills = list(set(skill_features))
    return top_job_skills


def feature_consolidation(resumes, top_unigram_list, top_bigram_list,  add_true_score=False):
    """
    Function to consolidate all the featuresets for the training data

    Args:
        resumes -- list of tuples [(resume_text, tag, filename), (resume_text, tag, filename)...]
        top_unigram_list -- list of top unigrams from the training dataset
        top_bigram_list -- list of top bigrams from the training dataset
        add_true_score -- boolean (default: False)

    Returns:
        consolidated_features -- list of consolidated features
    """
    uni_feats = [" ".join(unigram_features(resume_text, top_unigram_list)) for (resume_text, label, fname) in resumes]
    bi_feats = [" ".join(bigram_features(resume_text, top_bigram_list)) for (resume_text, label, fname) in resumes]
    consolidated_features = []
    ind = 0
    while ind < len(uni_feats):
        consolidated_features.append(uni_feats[ind] + bi_feats[ind])
        ind += 1
    return consolidated_features


def unigram_features(resume_text, top_unigram_list):
    """
    Function to create unigram features from the resume text

    Args:
        resume_text -- content of resume as string
        top_unigram_list -- list of top unigrams

    Returns:
        uni_features -- list of unigram features
    """
    resume_text = re.sub('[^A-Za-z\' ]+', '', str(resume_text))
    tokens = nltk.word_tokenize(resume_text.lower())
    tokens = [st.stem(token) for token in tokens]
    uni_features = []

    for tok in tokens:
        try:
            if tok in top_unigram_list:
                uni_features.append(tok)
        except UnicodeEncodeError:
            pass
    return uni_features


def bigram_features(resume_text, top_bigram_list):
    """
    Function to create bigram features from the resume text

    Args:
        resume_text -- content of resume as string
        top_bigram_list -- list of top bigrams

    Returns:
        bi_features -- list of bigram features
    """
    tokens = [st.stem(word) for word in resume_text.lower().split() if word not in stopwords]
    bigrs = bigrams(tokens)
    bigram_list = []
    bigram_list += [(bigrm[0], bigrm[1]) for bigrm in bigrs if (bigrm[0] not in stopwords and bigrm[1] not in stopwords)]
    bi_features = []

    for bi in bigram_list:
        if bi in top_bigram_list:
            bi_features.append(bi[0] + bi[1])
    return bi_features


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

    top_skills = extract_top_skills(train_resumes)

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
    tfidf_vect = TfidfVectorizer(stop_words='english')
    print "Create training resume tfidf"
    train_tfidf = tfidf_vect.fit_transform(train_resume_text)
    clf = trainsvm(train_tfidf, train_labels)

    print "Create testing resume counts"
    test_tfidf = tfidf_vect.transform(test_resume_text)

    # predicted = clf.predict(test_featureset)
    print "Predict testing labels"
    predicted = clf.predict(test_tfidf)
    # predicted_decision = clf.decision_function(test_featureset)
    predicted_decision = clf.decision_function(test_tfidf)

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

    # # CountVectorizer
    # count_vect = CountVectorizer(stop_words='english', vocabulary=top_skills)
    # print "Create training resume counts"
    # train_counts = count_vect.fit_transform(train_resume_text)
    # feats = count_vect.get_feature_names()
    # train_counts_array = train_counts.toarray()[0].tolist()
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

    # # TfidfVectorizer (unigrams + bigrams)
    # hash_uni_vect = HashingVectorizer(stop_words='english', ngram_range=(1, 1), n_features=20000, decode_error='ignore')
    # # hash_bi_vect = HashingVectorizer(stop_words='english', ngram_range=(2, 2), n_features=3000, decode_error='ignore')
    #
    # vectorizer = FeatureUnion([('uni', hash_uni_vect)])
    #
    # print "Create training resume hash"
    # train_hash = vectorizer.transform(train_resume_text)
    # clf = trainsvm(train_hash, train_labels)
    #
    # print "Create testing resume hash"
    # test_hash = vectorizer.transform(test_resume_text)
    #
    # print "Predict testing labels"
    # predicted_score = clf.predict(test_hash)
    # predicted_decision = clf.decision_function(test_hash)

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
    # with open('svmclassifier_new_0420_hash.pkl', 'wb') as outfile:
    #     pickle.dump(clf, outfile)
    #
    # with open('label_names_0420_hash.pkl', 'wb') as lab_names:
    #     pickle.dump(labels_names, lab_names)
    #
    # with open('hash_vect_0420_hash.pkl', 'wb') as hash_v:
    #     pickle.dump(vectorizer, hash_v)