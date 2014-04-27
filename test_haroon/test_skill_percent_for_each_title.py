"""
Verify functionality to extract skills from resume text.
"""

import os
import nltk
from nose.tools import *
from util import create_skills_map_with_percentage

nltk.data.path.append('nltk_data')

# Tests


class TestSkillsPercent:
    def __init__(self):
        self.current_file_directory = os.path.dirname(os.path.realpath(__file__))

    def test_should_return_100_percent_for_skill_present_in_both_sample_resumes(self):
        data = \
            [
                ("Some Text", "software developer", "14_plaintext.txt"),
                ("Some Text", "software developer", "15_plaintext.txt")
            ]
        xml_directory = self.current_file_directory + '/samples/'
        returned_skills_json_with_percent = create_skills_map_with_percentage(data, xml_directory, False)

        python_index = returned_skills_json_with_percent["software developer"]["skills"].index("Python")
        python_percent = returned_skills_json_with_percent["software developer"]["percent"][python_index]

        assert_equals(100, python_percent)

    def test_should_return_50_percent_for_skill_present_in_one_of_the_two_sample_resumes(self):
        data = \
            [
                ("Some Text", "software developer", "14_plaintext.txt"),
                ("Some Text", "software developer", "15_plaintext.txt")
            ]
        xml_directory = self.current_file_directory + '/samples/'
        returned_skills_json_with_percent = create_skills_map_with_percentage(data, xml_directory, False)

        java_index = returned_skills_json_with_percent["software developer"]["skills"].index("Java")
        java_percent = returned_skills_json_with_percent["software developer"]["percent"][java_index]

        assert_equals(50, java_percent)

    def test_should_return_skill_and_percent_lists_for_each_job_title(self):
        data = \
            [
                ("Some Text", "web developer", "13_plaintext.txt"),
                ("Some Text", "software developer", "14_plaintext.txt"),
                ("Some Text", "software developer", "15_plaintext.txt")
            ]
        xml_directory = self.current_file_directory + '/samples/'
        returned_skills_json_with_percent = create_skills_map_with_percentage(data, xml_directory, False)

        for key in returned_skills_json_with_percent:
            value = returned_skills_json_with_percent.get(key)
            assert_true(value)

# t = TestSkillsPercent()
# t.test_should_return_100_percent_for_skill_present_in_both_sample_resumes()
# t.test_should_return_50_percent_for_skill_present_in_one_of_the_two_sample_resumes()
# t.test_should_return_skill_and_percent_lists_for_each_job_title()
