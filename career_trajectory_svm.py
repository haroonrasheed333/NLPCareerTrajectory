from __future__ import division
import os
import random
import numpy as np
from nltk import bigrams
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.svm import LinearSVC, libsvm
from util import ResumeCorpus
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
    #label_dict = {'Administrative Assistant': 0, 'Assistant Manager': 1, 'Business Analyst': 2, 'Consultant': 3,
    #              'Customer Service Representative': 4, 'Director': 5, 'Graphic Designer': 6, 'Intern': 7,
    #              'Manager': 8, 'Marketing Manager': 9, 'President': 10, 'Project Manager': 11, 'Research Assistant': 12,
    #              'Sales Associate': 13, 'Senior Manager': 14, 'Senior Software Engineer': 15, 'Software Engineer': 16,
    #              'Vice President': 17, 'Web Developer': 18}
    #label_dict = {'Account Executive':0,'Account Manager':1,'Accountant':2,'Adjunct Faculty':3,
    #              'Administrative Assistant':4,'Analyst':5,'Assistant Manager':6,'Associate':7,'Business Analyst':8,
    #              'Business Development Manager':9,'Chief Information Officer':10,'Consultant':11,'Contractor':12,
    #              'Controller':13,'Customer Service Representative':14,'Director':15,'Executive Assistant':16,
    #              'Executive Director':17,'Financial Analyst':18,'General Manager':19,'Graphic Designer':20,
    #              'Independent Consultant':21,'Lead':22,'Manager':23,'Managing Director':24,'Marketing Consultant':25,
    #              'Marketing Director':26,'Marketing Manager':27,'Office Assistant':28,'Office Manager':29,
    #              'Operations Manager':30,'Owner':31,'President / Chief Executive Officer':32,'Product Manager':33,
    #              'Program Manager':34,'Project Manager':35,'Regional Manager':36,'Sales Associate':37,
    #              'Sales Consultant':38,'Sales Manager':39,'Sales Representative':40,'Senior Business Analyst':41,
    #              'Senior Consultant':42,'Senior Director':43,'Senior Manager':44,'Senior Project Manager':45,
    #              'Senior Software Engineer':46,'Software Engineer':47,'Vice President':48,'Web Developer':49}

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

    #label_dict1 = {0:'Account Executive',1:'Account Manager',2:'Accountant',3:'Adjunct Faculty',4:'Administrative Assistant',
    #               5:'Analyst',6:'Assistant Manager',7:'Associate',8:'Business Analyst',9:'Business Development Manager',
    #               10:'Chief Information Officer',11:'Consultant',12:'Contractor',13:'Controller',14:'Customer Service Representative',
    #               15:'Director',16:'Executive Assistant',17:'Executive Director',18:'Financial Analyst',19:'General Manager',
    #               20:'Graphic Designer',21:'Independent Consultant',22:'Lead',23:'Manager',24:'Managing Director',
    #               25:'Marketing Consultant',26:'Marketing Director',27:'Marketing Manager',28:'Office Assistant',
    #               29:'Office Manager',30:'Operations Manager',31:'Owner',32:'President / Chief Executive Officer',
    #               33:'Product Manager',34:'Program Manager',35:'Project Manager',36:'Regional Manager',37:'Sales Associate',
    #               38:'Sales Consultant',39:'Sales Manager',40:'Sales Representative',41:'Senior Business Analyst',
    #               42:'Senior Consultant',43:'Senior Director',44:'Senior Manager',45:'Senior Project Manager',
    #               46:'Senior Software Engineer',47:'Software Engineer',48:'Vice President',49:'Web Developer'}

    labels = []

    num_resumes = len(data_dict['label'])

    # Split the data training and test datasets
    train_resumes = data_dict['data'][0:int(num_resumes*0.9)]
    train_labels = data_dict['label'][0:int(num_resumes*0.9)]

    labels_names = sorted(list(set(train_labels)))

    count_vect = CountVectorizer()
    train_counts = vectorize(count_vect, train_resumes)
    tfidf_train = tfidftransform(train_counts)
    clf = trainsvm(tfidf_train, train_labels)

    test_resumes = data_dict['data'][int(num_resumes*0.9) + 1:]
    test_labels = data_dict['label'][int(num_resumes*0.9) + 1:]

    test_counts = count_vect.transform(test_resumes)
    tfidf_test = tfidftransform(test_counts)
    predicted = clf.predict(tfidf_test)
    predicted_decision = clf.decision_function(tfidf_test)

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