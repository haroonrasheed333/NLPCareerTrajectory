"""
Verify functionality to extract skills from resume text.
"""

import os
import nltk
from nose.tools import *
from util import create_skills_json

nltk.data.path.append('nltk_data')

# Tests


class TestSkillsExtraction:
    def __init__(self):
        self.job_title = 'software developer'
        self.resume_text_filename = 'Haroon_plaintext.txt'
        self.current_file_directory = os.path.dirname(os.path.realpath(__file__))
        self.resume_text = open(self.current_file_directory + '/' + self.resume_text_filename, 'rb').read()

    def test_should_extract_skills_from_skills_tag_of_xml_resume(self):
        expected_skills = ['xml', 'javascript', 'python', 'r', 'sql', 'css', 'html', 'git', 'php']
        data = [(self.resume_text, self.job_title, self.resume_text_filename)]
        returned_skills_json = create_skills_json(data, self.current_file_directory, False)
        returned_skills_list = returned_skills_json[self.job_title][0][self.resume_text_filename]

        for skill in expected_skills:
            assert_true(skill in returned_skills_list)

    # Actual skills tag from xml resume
    # <skills>Skills
    # C++, Python, HTML, JavaScript, jQuery, CSS, PHP, SQL, XML, XQuery, R, Git
    # Learning AngularJS</skills>

    def test_javascript_should_be_part_of_extracted_skills(self):
        data = [(self.resume_text, self.job_title, self.resume_text_filename)]
        returned_skills_json = create_skills_json(data, self.current_file_directory, False)
        returned_skills_list = returned_skills_json[self.job_title][0][self.resume_text_filename]

        # JavaScript is a noun
        word, tag = nltk.pos_tag(['javascript'])[0]
        assert_true(tag.startswith('NN'))

        # JavaScript should be a part of the returned skills as it is a noun
        assert_true('javascript' in returned_skills_list)

    def test_learning_should_not_be_part_of_extracted_skills(self):
        data = [(self.resume_text, self.job_title, self.resume_text_filename)]
        returned_skills_json = create_skills_json(data, self.current_file_directory, False)
        returned_skills_list = returned_skills_json[self.job_title][0][self.resume_text_filename]

        # Learning is not a noun
        word, tag = nltk.pos_tag(['learning'])[0]
        assert_false(tag.startswith('NN'))

        # Learning should not be a part of the returned skills as it is not a noun
        assert_false('learning' in returned_skills_list)
