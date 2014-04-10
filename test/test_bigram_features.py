"""
Verify bigrams feature functionality
"""

from nose.tools import *
from util import bigram_features

# Tests
sample_passing_text = """This function will extract all the skills from the training corpus and create a dictionary with
    Job Titles as keys and list of dictionaries containing the skills for each resume as values. The dictionary is
    converted and stored as a json file"""

sample_failing_text = """Function to create unigrams and remove stopwords from the data."""
top_bigrams = [('contain', 'skill'), ('convert', 'store'), ('corpu', 'creat'), ('creat', 'dictionari')]


def test_lengths_of_bigram_features_and_top_bigrams_should_be_equal():
    bigram_feats = bigram_features(sample_passing_text, top_bigrams)
    assert_equals(len(bigram_feats), len(top_bigrams))


def test_should_return_one_if_bigram_is_present_in_top_bigrams():
    bigram_feats = bigram_features(sample_passing_text, top_bigrams)
    for bi_feat in bigram_feats:
        assert_equals(1, bi_feat)


def test_should_return_zero_if_bigram_is_not_present_in_top_bigrams():
    bigram_feats = bigram_features(sample_failing_text, top_bigrams)
    for bi_feat in bigram_feats:
        assert_equals(0, bi_feat)