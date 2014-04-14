"""
Verify functionality to extract skills from resume text.
"""

import os
import nltk
from nose.tools import *
from util import create_skills_json

nltk.data.path.append('nltk_data')

# Tests
job_title = 'software developer'
resume_text_filename = 'Haroon_plaintext.txt'
current_file_directory = os.path.dirname(os.path.realpath(__file__))
resume_text = open(current_file_directory + '/' + resume_text_filename, 'rb').read()


def test_should_extract_skills_from_skills_tag_of_xml_resume():
    expected_skills = ['xml', 'javascript', 'python', 'r', 'sql', 'css', 'html', 'git', 'php']
    data = [(resume_text, job_title, resume_text_filename)]
    returned_skills_json = create_skills_json(data, current_file_directory, False)
    returned_skills_list = returned_skills_json[job_title][0][resume_text_filename]

    for skill in expected_skills:
        assert_true(skill in returned_skills_list)


# Actual skills tag from xml resume
# <skills>Skills
# C++, Python, HTML, JavaScript, jQuery, CSS, PHP, SQL, XML, XQuery, R, Git
# Learning AngularJS</skills>

def test_should_return_only_nouns_from_skills_tag():
    data = [(resume_text, job_title, resume_text_filename)]
    returned_skills_json = create_skills_json(data, current_file_directory, False)
    returned_skills_list = returned_skills_json[job_title][0][resume_text_filename]

    # JavaScript is a noun
    word, tag = nltk.pos_tag(['javascript'])[0]
    assert_true(tag.startswith('NN'))

    # Learning is not a noun
    word, tag = nltk.pos_tag(['learning'])[0]
    assert_false(tag.startswith('NN'))

    # JavaScript should be a part of the returned skills
    assert_true('javascript' in returned_skills_list)

    # Learning should not be a part of the returned skills
    assert_false('learning' in returned_skills_list)
