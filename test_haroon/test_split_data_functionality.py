import os
import nose
from nose.tools import *
from corpus_builder import prepare_data


class TestSplitData():
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

    def test_should_split_data_into_training_and_heldout_datasets(self):
        assert_true(os.path.exists(self.training_path))
        assert_true(os.path.exists(self.heldout_path))

        training_files = next(os.walk(self.training_path))[2]
        heldout_files = next(os.walk(self.heldout_path))[2]

        assert_true(len(training_files))
        assert_true(len(heldout_files))

    def test_should_create_label_files(self):
        assert_true(os.path.isfile(self.labels_file))
        assert_true(os.path.isfile(self.labels_heldout_file))

    def test_number_of_training_files_should_be_80_percent_of_sample_plaintext_files(self):
        training_files = next(os.walk(self.training_path))[2]
        plaintext_files = next(os.walk(self.plaintext_directory))[2]
        assert_equals(len(training_files), 0.8*len(plaintext_files))

    def test_number_of_heldout_files_should_be_20_percent_of_sample_plaintext_files(self):
        heldout_files = next(os.walk(self.heldout_path))[2]
        plaintext_files = next(os.walk(self.plaintext_directory))[2]
        assert_equals(len(heldout_files), 0.2*len(plaintext_files))

    def test_number_of_training_files_should_equal_the_number_of_items_in_labels_file(self):
        training_files = next(os.walk(self.training_path))[2]

        num_labels = len(open(self.labels_file).readlines())
        assert_equals(len(training_files), num_labels)

    def test_number_of_heldout_files_should_equal_the_number_of_items_in_heldout_labels_file(self):
        heldout_files = next(os.walk(self.heldout_path))[2]

        num_heldout_labels = len(open(self.labels_heldout_file).readlines())
        assert_equals(len(heldout_files), num_heldout_labels)

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


t = TestSplitData()
t.setup_class()
t.test_should_split_data_into_training_and_heldout_datasets()
t.test_should_create_label_files()
t.test_number_of_training_files_should_be_80_percent_of_sample_plaintext_files()
t.test_number_of_heldout_files_should_be_20_percent_of_sample_plaintext_files()
t.test_number_of_training_files_should_equal_the_number_of_items_in_labels_file()
t.test_number_of_heldout_files_should_equal_the_number_of_items_in_heldout_labels_file()
t.teardown_class()