from __future__ import division
import os
import re
import nltk
import random
import string
import pickle
from lxml import etree
from nltk import bigrams
from nltk import FreqDist
from collections import Counter
from util import ResumeCorpus

user_name = os.environ.get('USER')
punct = string.punctuation
stopwords = nltk.line_tokenize(open('stopwords.txt').read())
porter = nltk.PorterStemmer()


def create_skills_json(training_data):
    """
    This function will extract all the skills from the training corpus and create a dictionary with Job Titles as
    keys and list of all the skills for that Job Title as values

    Args:
        training_data -- list of tuples. Eg. [(resume, tag, filename), (resume, tag, filename)...]

    Returns:
        skills_dict -- A dictionary with Job Titles as keys and list of all the skills for that Job Title as values
    """

    skills_dict = dict()

    # Get the skills for each resume from its corresponding xml file.
    xml_directory = '/Users/' + user_name + '/Documents/Data/samples_1207'
    for (resume_text, tag_name, filename) in training_data:
        xml_file = filename.split('_')[0] + '.txt'
        xml = etree.parse(xml_directory + '/' + xml_file)
        skill_list = xml.xpath('//skills/text()')

        if skill_list:
            slist = []
            for skill in skill_list:
                try:
                    skill = str(skill).encode('utf-8')
                except:
                    skill = skill.encode('utf-8')
                skill = skill.translate(None, ',:();-')
                skill = skill.replace('/', ' ')
                skill = skill.rstrip('.')
                skill_words = nltk.word_tokenize(skill)

                skill_words_nouns = [
                    porter.stem(w.lower()) for (w, t) in nltk.pos_tag(skill_words) if t == 'NNP'
                    and w.lower() not in stopwords
                ]

                skill_words_nouns = list(set(skill_words_nouns))
                slist += skill_words_nouns

            value = skills_dict.get(tag_name, None)
            if value is not None:
                skills_dict[tag_name] = value + slist
            else:
                skills_dict[tag_name] = []
                skills_dict[tag_name] = slist

    return skills_dict


def extract_top_skills(training_data):
    """
    Extract Top Skills for each Job Title from the training dataset.

    Args:
        training_data -- list of tuples. Eg. [(resume, tag, filename), (resume, tag, filename)...]

    Returns:
        A consolidated list of top skills for all the Job Titles

    """
    skills_dict = create_skills_json(training_data)

    # Read the top n skills for each Job TiTle
    skill_features = []
    for skill in skills_dict:
        skill_list = skills_dict[skill]
        skill_count = Counter(skill_list)
        top_job_skills = sorted(skill_count, key=skill_count.get, reverse=True)[:150]
        skill_features += top_job_skills

    top_job_skills = list(set(skill_features))
    return top_job_skills


def train_classifier(training_featureset):
    """
    Function to train the naive bayes classifier using the training features

    Args:
        training_featureset -- dictionary of training features

    Returns:
        rev_classifier -- NaiveBayes classifier object
    """
    rev_classifier = nltk.NaiveBayesClassifier.train(training_featureset)
    return rev_classifier


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
    if add_true_score:
        uni_feats = [(unigram_features(resume_text, top_unigram_list), label) for (resume_text, label, fname) in resumes]
        bi_feats = [(bigram_features(resume_text, top_bigram_list), label) for (resume_text, label, fname) in resumes]
        consolidated_features = uni_feats + bi_feats
    else:
        uni_feats = unigram_features(resumes, top_unigram_list)
        bi_feats = bigram_features(resumes, top_bigram_list)
        consolidated_features = dict(uni_feats.items() + bi_feats.items())
    return consolidated_features


def unigram_features(resume_text, top_unigram_list):
    """
    Function to create unigram features from the resume text

    Args:
        resume_text -- content of resume as string
        top_unigram_list -- list of top unigrams

    Returns:
        uni_features -- dictionary of unigram features
    """
    resume_text = re.sub('[^A-Za-z\' ]+', '', str(resume_text))
    tokens = nltk.word_tokenize(resume_text)
    uni_features = {}
    avg_word_len= 0
    count = 0
    for token in tokens:
        token_stem = str(porter.stem(token))
        if token_stem in top_unigram_list:
            uni_features[token_stem] = True
            avg_word_len += len(token_stem)
            count += 1
    uni_features['average_word_length'] = avg_word_len/(count+1)
    uni_features['docu_length'] = len(tokens)
    return uni_features


def bigram_features(resume_text, top_bigram_list):
    """
    Function to create bigram features from the resume text

    Args:
        resume_text -- content of resume as string
        top_bigram_list -- list of top bigrams

    Returns:
        bi_features -- dictionary of bigram features
    """
    tokens = nltk.word_tokenize(resume_text)
    bigrs = bigrams(tokens)
    bigram_list = []
    bigram_list += [(bigrm[0], bigrm[1]) for bigrm in bigrs if (bigrm[0] not in stopwords or bigrm[1] not in stopwords)]
    bi_features = {}
    for bigram in bigram_list:
        if bigram in top_bigram_list:
            bi_features[bigram] = True
    return bi_features


def main():
    traintest_corpus = ResumeCorpus('/Users/' + user_name + '/Documents/Data')

    # Shuffle the corpus
    random.seed()
    random.shuffle(traintest_corpus.resumes)

    # Use 90% of the shuffled corpus as training and remaining 10% as testing datasets
    num_resumes = len(traintest_corpus.resumes)
    train_resumes = traintest_corpus.resumes[0:int(num_resumes*0.9)]
    test_resumes = traintest_corpus.resumes[int(num_resumes*0.9) + 1:]

    # Extract the top skills from the training data
    top_skills = extract_top_skills(train_resumes)

    # Extract the top unigrams and bigrams from the training data
    words = []
    bigrams_list = []
    for resume in train_resumes:
        unigrams = resume[0].lower().split()
        words = words + unigrams
        bigrms = bigrams(unigrams)
        bigrams_list += [(bigr[0], bigr[1]) for bigr in bigrms if (bigr[0] not in stopwords and bigr[1] not in stopwords)]

    fd = FreqDist(words)
    fd_bi = FreqDist(bigrams_list)

    top_unigrams = [porter.stem(word) for word in fd.keys()[:500] if word not in stopwords]
    top_unigrams = list(set(top_unigrams + top_skills))
    top_bigrams = fd_bi.keys()[:200]

    # Create a training featureset from the top unigrams, skills and bigrams.
    train_featureset = feature_consolidation(train_resumes, top_unigrams, top_bigrams, True)

    # Train a Naive Bayes classifier using the training featureset
    review_classifier = train_classifier(train_featureset)

    # Create a test featureset.
    test_featureset = feature_consolidation(test_resumes, top_unigrams, top_bigrams, True)

    # Classify the test featureset using the trained classifier and find the accuracy
    accuracy = nltk.classify.accuracy(review_classifier, test_featureset)
    print accuracy

    # Print the 50 most informative features
    review_classifier.show_most_informative_features(50)

    # Classify each test resume using the trained classifier and compare the actual vs. classified label.
    # Write output to a file.
    output_file = open('classifier_output.txt','w')
    for document in test_resumes:
        resume_features = feature_consolidation(document[0], top_unigrams, top_bigrams)
        (text, tag, file_name) = document
        classifier_output = review_classifier.classify(resume_features)
        output_file.write('%s' % file_name + '\t' + '%s' % str(tag) + '\t' + '%s' % classifier_output + '\n')
    output_file.close()

    # Pickle the classifier and training features to test it on the heldout dataset.
    with open('nbclassifier.pkl', 'wb') as outfile:
        pickle.dump(review_classifier, outfile)

    features = dict()
    features['top_unigrams'] = top_unigrams
    features['top_bigrams'] = top_bigrams

    with open('features.pkl', 'wb') as f:
        pickle.dump(features, f)


if __name__ == "__main__":
    main()