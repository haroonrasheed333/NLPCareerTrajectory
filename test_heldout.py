import os
import nltk
import pickle
from career_trajectory import feature_consolidation


class ResumeCorpus():
    """
    Class to read the source files from source directory and create a list of tuples with resume_text, tag and filename
    for each resume.

    Args:
        source_dir -- string. The path of the source directory.
        labels_file -- string. The path of the labels file (default: None)
    """
    def __init__(self, source_dir, labels_file=None):

        self.source_dir = source_dir
        if not labels_file:
            self.labels_file = self.source_dir + '/labels_heldout.txt'
        else:
            self.labels_file = labels_file
        self.resumes = self.read_files()

    def read_files(self):
        """
        Method to return a list of tuples with resume_text, tag and filename for the training data

        Args:
            No Argument

        Returns:
            resumes -- list of tuples with resume_text, tag and filename for the training data
        """
        resumes = []

        for line in open(self.labels_file).readlines():
            try:
                filename_tag = line.split('\t')
                filename = filename_tag[0]
                resume_tag = filename_tag[1].rstrip()
                resumes.append((open(self.source_dir + '/heldout/' + filename).read(), resume_tag, filename))
            except IOError, (ErrorNumber, ErrorMessage):
                if ErrorNumber == 2:
                    pass

        return resumes


def main():
    """
    Test the heldout dataset using the trained classifier and features
    """

    # Get the pickled classifier model and features
    with open('nbclassifier.pkl', 'rb') as infile:
        model = pickle.load(infile)

    with open('features.pkl', 'rb') as f:
        features = pickle.load(f)

    top_unigrams = features['top_unigrams']
    top_bigrams = features['top_bigrams']

    model.show_most_informative_features(50)

    # Create a corpus from the heldout data
    user_name = os.environ.get('USER')
    heldout_corpus = ResumeCorpus('/Users/' + user_name + '/Documents/Data')

    # Create a featureset for the heldout data
    heldout_featureset = feature_consolidation(heldout_corpus.resumes, top_unigrams, top_bigrams, True)

    # Classify the heldout corpus using the trained classifier and find the accuracy.
    accuracy = nltk.classify.accuracy(model, heldout_featureset)
    print accuracy

if __name__ == '__main__':
    main()