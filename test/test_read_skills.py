"""
Test to verify skill creation from json
"""

from nose.tools import eq_
from util import read_skills_from_json_file

# Tests

def test_skills_dict_must_be_created():
	training_data =[("Responsible for developing and implementing a high level security feature in the homepage","Software Engineer", "plain_text1.txt")]
	x = read_skills_from_json_file(training_data)
	

