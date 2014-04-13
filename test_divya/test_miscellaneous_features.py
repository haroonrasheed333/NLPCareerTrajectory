"""
Test to verify miscellaneous feature extraction from a given resume text
"""

from nose.tools import eq_
from util import miscellaneous_features

# Tests

def test_miscellaneous_features_created():
	file = open("test_resume.txt","r")
	raw_text = file.read()
	feature_dict = miscellaneous_features(raw_text)
	length_of_features = 4
	eq_(length_of_features, len(feature_dict))


def test_length_of_resume_must_equal_words():
	file = open("test_resume.txt","r")
        raw_text = file.read()
        feature_dict = miscellaneous_features(raw_text)
        length_of_resume = 39
        eq_(length_of_resume, feature_dict["length"])	

def test_number_of_adjectives():

	file = open("test_resume.txt","r")
        raw_text = file.read()
        feature_dict = miscellaneous_features(raw_text)
        adjectives = 6
        eq_(adjectives, feature_dict["adj_count"])

def test_number_of_nouns():
	file = open("test_resume.txt","r")
        raw_text = file.read()
        feature_dict = miscellaneous_features(raw_text)
        nouns = 12
        eq_(nouns, feature_dict["noun_count"])

def test_avg_word_length():

	file = open("test_resume.txt","r")
        raw_text = file.read()
        feature_dict = miscellaneous_features(raw_text)
        avg_word_length = 6
        eq_(avg_word_length, feature_dict["avg_word_length"])


