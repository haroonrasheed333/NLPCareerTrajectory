"""
Verify corpus builder functionality
"""
import os
from nose.tools import *
from corpus_builder_old import prepare_data


# List of sample resume filenames with their present job title
# 1.txt  Software Engineer
# 2.txt	 Senior Software Engineer
# 3.txt	 Software Developer
# 4.txt	 No present job
# 5.txt	 Web Developer
# 6.txt	 Business Analyst
# 7.txt	 No present job
# 8.txt	 Project Manager
# 9.txt	 Graphic Designer
# 10.txt Sr. Project Manager
# 11.txt Intern (Not a top job title)
# 12.txt CEO
# 13.txt VP


class TestCorpusBuilder:
    def __init__(self):
        self.paths = dict()
        self.paths['main_source_directory'] = os.path.dirname(os.path.realpath(__file__))
        self.paths['xml_data_directory'] = 'samples'
        self.paths['plaintext_data_directory'] = 'samples_text'
        self.paths['training_directory'] = 'training'
        self.paths['heldout_directory'] = 'heldout'
        self.paths['labels_file_path'] = 'labels.txt'
        self. paths['labels_heldout_file_path'] = 'labels_heldout.txt'
        self.plaintext_directory = self.paths['main_source_directory'] + '/' + self.paths['plaintext_data_directory']
        self.labels_file = self.paths['main_source_directory'] + '/' + self.paths['labels_file_path']
        self.labels_heldout_file = self.paths['main_source_directory'] + '/' + self.paths['labels_heldout_file_path']
        self.training_path = self.paths['main_source_directory'] + '/' + self.paths['training_directory']
        self.heldout_path = self.paths['main_source_directory'] + '/' + self.paths['heldout_directory']

    @classmethod
    def setup_class(cls):
        """
        Nose will execute this function before executing the tests.
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

        prepare_data(self.paths)

    @classmethod
    def teardown_class(cls):
        """
        Nose will execute this function after executing all the tests.
        Remove files generated during test runs
        """
        self = cls()
        self.remove_files_created_during_previous_runs()

    def test_should_extract_resume_content_from_xml_files_and_save_as_plaintext_files(self):
        filenames = next(os.walk(self.plaintext_directory))[2]
        assert_true(len(filenames))

    def test_should_not_select_resumes_without_present_job(self):
        resumes_without_present_job = ['4_plaintext.txt', '7_plaintext.txt']
        plaintext_files = next(os.walk(self.plaintext_directory))[2]

        for f in resumes_without_present_job:
            assert_false(f in plaintext_files)

    def test_should_not_select_resumes_with_present_job_not_in_top_jobs(self):
        resumes_with_present_job_not_in_top_jobs = ['11_plaintext.txt']
        plaintext_files = next(os.walk(self.plaintext_directory))[2]

        for f in resumes_with_present_job_not_in_top_jobs:
            assert_false(f in plaintext_files)

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


# t = TestCorpusBuilder()
# t.setup_class()
# t.test_should_extract_resume_content_from_xml_files_and_save_as_plaintext_files()
# t.test_should_not_select_resumes_without_present_job()
# t.test_should_not_select_resumes_with_present_job_not_in_top_jobs()
# t.teardown_class()