"""
Validate functionality to clean and extract job titles
"""

import os
from lxml import etree
from nose.tools import *
from corpus_builder_old import clean_data_and_extract_job_titles


class TestCleanDataAndExtractJobTitles():
    def __init__(self):
        self.paths = dict()
        self.paths['main_source_directory'] = os.path.dirname(os.path.realpath(__file__))
        self.paths['xml_data_directory'] = 'samples'
        self.paths['plaintext_data_directory'] = 'samples_text'
        self.paths['training_directory'] = 'training'
        self.paths['heldout_directory'] = 'heldout'
        self.paths['labels_file_path'] = 'labels.txt'
        self.paths['labels_heldout_file_path'] = 'labels_heldout.txt'
        self.plaintext_directory = self.paths['main_source_directory'] + '/' + self.paths['plaintext_data_directory']
        self.labels_file = self.paths['main_source_directory'] + '/' + self.paths['labels_file_path']
        self.labels_heldout_file = self.paths['main_source_directory'] + '/' + self.paths['labels_heldout_file_path']
        self.training_path = self.paths['main_source_directory'] + '/' + self.paths['training_directory']
        self.heldout_path = self.paths['main_source_directory'] + '/' + self.paths['heldout_directory']
        self.xml_files_path = self.paths['main_source_directory'] + '/' + self.paths['xml_data_directory']

    @classmethod
    def setup_class(cls):
        """
        Nose will execute setup_class before executing the tests in the class.
        Remove all the files generated during previous test runs, create necessary directories and run the prepare
        data function
        """
        self = cls()
        self.remove_files_created_during_previous_runs()
        if not os.path.exists(self.plaintext_directory):
            os.makedirs(self.plaintext_directory)

        if not os.path.exists(self.training_path):
            os.makedirs(self.training_path)

        if not os.path.exists(self.heldout_path):
            os.makedirs(self.heldout_path)

    @classmethod
    def teardown_class(cls):
        """
        Nose will execute teardown_class after executing all the tests.
        Remove files generated during test runs
        """
        self = cls()
        self.remove_files_created_during_previous_runs()

    def test_cleaned_resume_data_should_not_have_candidate_name(self):
        (names, job_titles, labels_list) = clean_data_and_extract_job_titles("1.txt", self.paths, [], [], [])
        candidate_name = names[0].split()
        plaintext_filename = labels_list[0][0]
        plaintext_data = open(self.plaintext_directory + '/' + plaintext_filename).read()

        for n in candidate_name:
            assert_false(n in plaintext_data)

    def test_cleaned_resume_data_should_not_have_candidate_contact(self):
        (names, job_titles, labels_list) = clean_data_and_extract_job_titles("1.txt", self.paths, [], [], [])
        resume_xml = etree.parse(self.xml_files_path + '/1.txt')
        candidate_phone = resume_xml.xpath('//phone/text()')[0]
        plaintext_filename = labels_list[0][0]
        plaintext_data = open(self.plaintext_directory + '/' + plaintext_filename).read()

        assert_false(candidate_phone in plaintext_data)

    def test_cleaned_resume_data_should_not_have_present_job_information(self):
        (names, job_titles, labels_list) = clean_data_and_extract_job_titles("1.txt", self.paths, [], [], [])
        present_job_title = job_titles[0]
        plaintext_filename = labels_list[0][0]
        plaintext_data = open(self.plaintext_directory + '/' + plaintext_filename).read()

        assert_false(present_job_title in plaintext_data)

    def test_present_job_title_should_match_resume_label(self):
        (names, job_titles, labels_list) = clean_data_and_extract_job_titles("1.txt", self.paths, [], [], [])
        present_job_title = job_titles[0]
        resume_label = labels_list[0][1]

        assert_equals(present_job_title, resume_label)

    def remove_files_created_during_previous_runs(self):
        for root, dirs, files in os.walk(self.plaintext_directory, topdown=False):
            for f in files:
                os.remove(os.path.join(root, f))
            for d in dirs:
                os.rmdir(os.path.join(root, d))
            if os.path.exists(root):
                os.rmdir(root)

        if os.path.isfile(self.labels_file):
            os.remove(self.labels_file)
        if os.path.isfile(self.labels_heldout_file):
            os.remove(self.labels_heldout_file)

        for root, dirs, files in os.walk(self.training_path, topdown=False):
            for f in files:
                os.remove(os.path.join(root, f))
            for d in dirs:
                os.rmdir(os.path.join(root, d))
            if os.path.exists(root):
                os.rmdir(root)

        for root, dirs, files in os.walk(self.heldout_path, topdown=False):
            for f in files:
                os.remove(os.path.join(root, f))
            for d in dirs:
                os.rmdir(os.path.join(root, d))
            if os.path.exists(root):
                os.rmdir(root)


t = TestCleanDataAndExtractJobTitles()
t.setup_class()
t.test_cleaned_resume_data_should_not_have_candidate_name()
t.test_cleaned_resume_data_should_not_have_candidate_contact()
t.test_cleaned_resume_data_should_not_have_present_job_information()
t.test_present_job_title_should_match_resume_label()
t.teardown_class()