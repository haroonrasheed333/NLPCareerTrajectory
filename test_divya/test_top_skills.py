"""
Test to verify top skills created for a training data set
"""

from nose.tools import eq_
from util import read_skills_from_json_file
from util import extract_top_skills

# Tests


def test_if_top_3_skills_are_genetared():

	training_data =[("Responsible for developing and implementing a high level security feature in the homepage","vice president", "327099_plaintext.txt")]
	expected_value = 3
	skills_list = extract_top_skills(training_data)
	eq_(expected_value,len(skills_list))


def test_top_skill_for_test_text_is_softwar():
	training_data =[("Responsible for developing and implementing a high level security feature in the homepage","vice president", "327099_plaintext.txt")]
        expected_value = 'softwar'
        skills_list = extract_top_skills(training_data)
        eq_(expected_value,unicode(skills_list[0]))


def test_for_file_not_in_list_returns_null():

	training_data =[("Responsible for developing and implementing a high level security feature in the homepage","vice president", "1_plaintext.txt")]
        expected_value = 0
        skills_list = extract_top_skills(training_data)
        eq_(expected_value,len(skills_list))

