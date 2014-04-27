"""
Test to verify if university name is extracetd form test resume
"""

from nose.tools import eq_
from univ_lookup import extract_from_resume
from util import stripxml

# Tests

def test_if_resume_split_at_word_education_and_takes_150_characters_after():
    test_resume =open("test_divya/samples/13.txt","rb").read()
    test_resume = str(test_resume)
    result = extract_from_resume(test_resume)
    eq_(150, len(result['split2']))

def test_if_resume_split_at_education():
    test_resume =open("test_divya/samples/13.txt","rb").read()
    test_resume = str(test_resume)
    result = extract_from_resume(test_resume)
    eq_("university", str(result['split2'][:11]).strip().lower())

def test_if_extracted_univ_is_berkeley():
    test_resume =open("test_divya/samples/13.txt","rb").read()
    test_resume = str(test_resume)
    result = extract_from_resume(test_resume)
    eq_("University of California Berkeley", str(result['univ']).strip())

def test_if_extracted_univ_is_curry_college():
    test_resume =open("test_divya/samples/14.txt","rb").read()
    test_resume = str(test_resume)
    result = extract_from_resume(test_resume)
    eq_("Curry College", str(result['univ']).strip())

def test_if_extracted_univ_is_curry_college():
    test_resume =open("test_divya/samples/14.txt","rb").read()
    test_resume = str(test_resume)
    result = extract_from_resume(test_resume)
    eq_("Curry College", str(result['univ']).strip())