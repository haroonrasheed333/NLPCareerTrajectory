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


def main():
    """
    Test the heldout dataset using the trained classifier and features
    """
    resume_text = [open('HNew.txt').read()]

    # Get the pickled classifier model and features
    with open('svmclassifier_new_0420_marisa.pkl', 'rb') as infile:
        model = pickle.load(infile)

    with open('label_names_0420_marisa.pkl', 'rb') as lab_names:
        labels_names = pickle.load(lab_names)

    with open('hash_vect_0420_marisa.pkl', 'rb') as tfidf_v:
        tfidf_vect = pickle.load(tfidf_v)

    test_resumes = resume_text

    test_tfidf = tfidf_vect.transform(test_resumes)
    predicted_score = model.predict(test_tfidf)
    predicted_decision = model.decision_function(test_tfidf)

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