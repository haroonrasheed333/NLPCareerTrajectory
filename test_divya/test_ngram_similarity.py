"""
Test to verify if similarity score is computed to extract university name
"""

from nose.tools import eq_
from univ_lookup import ngram_similarity

# Tests

def test_ngram_similarity_returns_score():
    test_string_1 = "University of California"
    score = ngram_similarity(test_string_1)
    eq_(float,type(score['score']))


def test_ngram_similarity_returns_univ_similarity_score():
    test_string_1 = "University of California"
    score = ngram_similarity(test_string_1)
    eq_(0.57,int(score['score'] * 100) / 100.0)

def test_ngram_similarity_returns_score_1():
    test_string_1 = "University of California Berkeley"
    score = ngram_similarity(test_string_1)
    eq_(0.5,int(score['score_used'] * 100) / 100.0)

def test_ngram_similarity_returns_univ_name_berkeley():
    test_string_1 = "University of California Berkeley"
    score = ngram_similarity(test_string_1)
    eq_("university of california berkeley", str(score['univ']).strip().lower())

def test_ngram_similarity_returns_univ_name_curry_college():
    test_string_1 = "Curry College"
    score = ngram_similarity(test_string_1)
    eq_("curry college", str(score['univ']).strip().lower())