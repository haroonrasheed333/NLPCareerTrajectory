"""
Validate degree level extraction functionality
"""
import os
from nose.tools import *
from util2 import get_degree_level_from_resume


class TestDegreeLevel():
    def __init__(self):
        self.current_file_directory = os.path.dirname(os.path.realpath(__file__))
        self.sample_resume_directory = self.current_file_directory + '/samples_degree_level/'
        self.masters_resume = self.sample_resume_directory + 'Masters.txt'
        self.bachelors_resume = self.sample_resume_directory + 'Bachelors.txt'
        self.phd_resume = self.sample_resume_directory + 'Phd.txt'
        self.diploma_resume = self.sample_resume_directory + 'Diploma.txt'
        self.no_education_resume = self.sample_resume_directory + 'NoEducation.txt'


    @classmethod
    def setup_class(cls):
        """
        Nose will execute setup_class before executing the tests in the class.
        """

    @classmethod
    def teardown_class(cls):
        """
        Nose will execute teardown_class after executing all the tests.
        """

    def test_should_return_point_zero_two_one_for_phd_resume(self):
        resume_text = open(self.phd_resume).read()
        resume_data = [(resume_text, "Phd", "Phd.txt")]
        degree_level = get_degree_level_from_resume(resume_data)
        assert_equals(0.021, degree_level[0])

    def test_should_return_point_zero_one_eight_for_masters_resume(self):
        resume_text = open(self.masters_resume).read()
        resume_data = [(resume_text, "Masters", "Masters.txt")]
        degree_level = get_degree_level_from_resume(resume_data)
        assert_equals(0.018, degree_level[0])

    def test_should_return_point_zero_one_six_for_bachelors_resume(self):
        resume_text = open(self.bachelors_resume).read()
        resume_data = [(resume_text, "Bachelors", "Bachelors.txt")]
        degree_level = get_degree_level_from_resume(resume_data)
        assert_equals(0.016, degree_level[0])

    def test_should_return_point_zero_one_three_for_diploma_resume(self):
        resume_text = open(self.diploma_resume).read()
        resume_data = [(resume_text, "Diploma", "Diploma.txt")]
        degree_level = get_degree_level_from_resume(resume_data)
        assert_equals(0.013, degree_level[0])

    def test_should_return_zero_if_degree_is_not_found(self):
        resume_text = open(self.no_education_resume).read()
        resume_data = [(resume_text, "NoEducation", "NoEducation.txt")]
        degree_level = get_degree_level_from_resume(resume_data)
        assert_equals(0, degree_level[0])


# t = TestDegreeLevel()
# t.setup_class()
# t.test_should_return_point_zero_two_one_for_phd_resume()
# t.test_should_return_point_zero_one_eight_for_masters_resume()
# t.test_should_return_point_zero_one_six_for_bachelors_resume()
# t.test_should_return_point_zero_one_three_for_diploma_resume()
# t.test_should_return_zero_if_degree_is_not_found()
# t.teardown_class()