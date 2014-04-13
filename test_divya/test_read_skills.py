"""
Test to verify skill creation from json
"""

from nose.tools import eq_
from util import read_skills_from_json_file

# Tests

def test_skills_dict_length_must_be_same_as_input_files_length():
	training_data =[("Responsible for developing and implementing a high level security feature in the homepage","vice president", "327099_plaintext.txt")]
	expected_value = 1 
	skills_dict = read_skills_from_json_file(training_data)
	eq_(expected_value,len(skills_dict))


def test_skills_dict_value_must_be_from_skils_file_for_title():

	training_data =[("Responsible for developing and implementing a high level security feature in the homepage","sales manager", "67255_plaintext.txt")]
        expected_value = "salesforcecom"
        skills_dict = read_skills_from_json_file(training_data)
	if expected_value in skills_dict["sales manager"]:
		skill_added = 1
        eq_(1,skill_added)


def test_add_skills_only_if_file_in_json():

	training_data =[("Responsible for developing and implementing a high level security feature in the homepage","sales manager", "1_plaintext.txt")]
        expected_value = 0
        skills_dict = read_skills_from_json_file(training_data)
        
        eq_(expected_value,len(skills_dict))
