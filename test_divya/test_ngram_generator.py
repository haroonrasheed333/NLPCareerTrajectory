"""
Test to verify if n grams of varied lengths are generated form given input string
"""

from nose.tools import eq_
from univ_lookup import generate_ngrams

# Tests

def test_generate_ngrams_creates_5_ngrams_list():
    input = "i am testing ngram generation"
    output = generate_ngrams(input)
    eq_(4, len(output))

def test_generate_ngrams_creates_4_ngrams_of_length_2():
    input = "i am testing ngram generation"
    output = generate_ngrams(input)
    eq_(4, len(output[2]))

def test_generate_ngrams_creates_3_ngrams_of_length_3():
    input = "i am testing ngram generation"
    output = generate_ngrams(input)
    eq_(3, len(output[3]))

def test_generate_ngrams_creates_2_ngrams_of_length_4():
    input = "i am testing ngram generation"
    output = generate_ngrams(input)
    eq_(2, len(output[4]))

def test_first_bigram_is_i_am():
    input = "i am testing ngram generation"
    output = generate_ngrams(input)
    eq_(('i','am'), output[2][0])

def test_first_4gram_is_i_am_testing_ngram():
    input = "i am testing ngram generation"
    output = generate_ngrams(input)
    eq_(('i','am','testing','ngram'), output[4][0])

def test_second_3gram_is_i_am_testing_ngram():
    input = "i am testing ngram generation"
    output = generate_ngrams(input)
    eq_(('am','testing','ngram'), output[3][1])
