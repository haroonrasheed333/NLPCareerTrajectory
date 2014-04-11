from __future__ import division
import os
import json
import random
import pickle
from nltk import bigrams
from nltk import FreqDist
from collections import Counter
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.svm import LinearSVC
from util import ResumeCorpus, unigram_features, bigram_features
from collections import defaultdict

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
    temp_dict = json.loads(open("skills.json").read())
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
        top_job_skills = sorted(skill_count, key=skill_count.get, reverse=True)[:300]
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
    uni_feats = [unigram_features(resume_text, top_unigram_list) for (resume_text, label, fname) in resumes]
    bi_feats = [bigram_features(resume_text, top_bigram_list) for (resume_text, label, fname) in resumes]
    consolidated_features = []
    ind = 0
    while ind < len(uni_feats):
        consolidated_features.append(uni_feats[ind] + bi_feats[ind])
        ind += 1
    return consolidated_features


def trainsvm(featureset, train_label):
    clf = LinearSVC().fit(featureset, train_label)
    return clf


if __name__ == '__main__':
    user_name = os.environ.get('USER')
    traintest_corpus = ResumeCorpus('/Users/' + user_name + '/Documents/Data')

    # Shuffle the corpus
    random.seed()
    random.shuffle(traintest_corpus.resumes)

    # Use 90% of the shuffled corpus as training and remaining 10% as testing datasets
    num_resumes = len(traintest_corpus.resumes)

    # Split the data training and test datasets
    train_resumes = traintest_corpus.resumes[0:int(num_resumes*0.9)]
    test_resumes = traintest_corpus.resumes[int(num_resumes*0.9) + 1:]

    # train_resumes = traintest_corpus.resumes[0:20]
    # test_resumes = traintest_corpus.resumes[20:25]

    train_labels = []
    for (text, label, fname) in train_resumes:
        train_labels.append(label)

    test_labels = []
    for (text, label, fname) in test_resumes:
        test_labels.append(label)

    labels_names = sorted(list(set(train_labels)))

    # Extract the top skills from the training data
    top_skills = extract_top_skills(train_resumes)

    # Extract the top unigrams and bigrams from the training data
    words = []
    bigrams_list = []
    for resume in train_resumes:
        unigrams = [st.stem(word) for word in resume[0].lower().split() if word not in stopwords]
        words = words + unigrams
        bigrms = bigrams(unigrams)
        bigrams_list += [(bigr[0], bigr[1]) for bigr in bigrms if (bigr[0] not in stopwords and bigr[1] not in stopwords)]

    fd = FreqDist(words)
    fd_bi = FreqDist(bigrams_list)

    print len(words)
    print len(bigrams_list)

    top_unigrams = fd.keys()[:4000]
    top_unigrams = list(set(top_unigrams + top_skills))
    top_bigrams = fd_bi.keys()[:4000]

    # Create a training featureset from the top unigrams, skills and bigrams.
    train_featureset = feature_consolidation(train_resumes, top_unigrams, top_bigrams, True)
    clf = trainsvm(train_featureset, train_labels)

    test_featureset = feature_consolidation(test_resumes, top_unigrams, top_bigrams, True)

    predicted = clf.predict(test_featureset)
    predicted_decision = clf.decision_function(test_featureset)

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
    with open('svmclassifier_new.pkl', 'wb') as outfile:
        pickle.dump(clf, outfile)

    features = dict()
    features['top_unigrams'] = top_unigrams
    features['top_bigrams'] = top_bigrams

    with open('features.pkl', 'wb') as f:
        pickle.dump(features, f)

    with open('label_names.pkl', 'wb') as lab_names:
        pickle.dump(labels_names, lab_names)