from __future__ import division
import pickle
from nltk import bigrams
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from career_trajectory_svm import tfidftransform
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
    resume_text = open('Div.txt').read()

    try:
        resume_text = pre_processing(resume_text)
        resume_text = " ".join(resume_text)
        data_dict['data'].append(resume_text)
    except:
        pass


def main():
    """
    Test the heldout dataset using the trained classifier and features
    """
    prepare_data()

    # Get the pickled classifier model and features
    with open('svmclassifier.pkl', 'rb') as infile:
        model = pickle.load(infile)

    with open('label_names.pkl', 'rb') as lab_names:
        labels_names = pickle.load(lab_names)

    with open('count_vect.pkl', 'rb') as count_v:
        count_vect = pickle.load(count_v)

    test_resumes = data_dict['data'][:]

    test_counts = count_vect.transform(test_resumes)
    tfidf_test = tfidftransform(test_counts)
    predicted_score = model.predict(tfidf_test)
    predicted_decision = model.decision_function(tfidf_test)

    predicted = []

    for i in range(1):
        predicted_dec_dup = predicted_decision[i]
        predicted_dec_dup_sorted = sorted(predicted_dec_dup, reverse=True)
        top_five_predictions = []
        predicted.append(labels_names[predicted_decision[i].tolist().index(predicted_dec_dup_sorted[0])])
        for j in range(5):
            top_five_predictions.append(labels_names[predicted_decision[i].tolist().index(predicted_dec_dup_sorted[j])])

        print "Predicted top5: " + ", ".join(top_five_predictions)


if __name__ == '__main__':
    main()