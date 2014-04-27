"""
Verify functionality to extract features for network map.
"""

import os
import nltk
from lxml import etree
from nose.tools import *
from util import extract_features_for_network_map

nltk.data.path.append('nltk_data')

# Tests


class TestNetworkMap:
    def __init__(self):
        self.current_file_directory = os.path.dirname(os.path.realpath(__file__))
        self.xml_file_directory = self.current_file_directory + '/samples'

    def test_should_return_an_empty_dict_for_invalid_xml_directory(self):
        xml_directory = self.current_file_directory + '/invalid_path/'
        returned_education_job_map_dict = extract_features_for_network_map(xml_directory, False)

        assert_equals({}, returned_education_job_map_dict)

    def test_returned_education_job_map_dict_should_have_mapping_for_all_xml_resumes(self):
        returned_education_job_map_dict = extract_features_for_network_map(self.xml_file_directory, False)
        path, dirs, files = next(os.walk(self.xml_file_directory))

        assert_equals(len(files), len(returned_education_job_map_dict))

    def test_university_name_should_match_in_returned_dict_and_xml_file(self):
        returned_education_job_map_dict = extract_features_for_network_map(self.xml_file_directory, False)
        xml_file_name = "1.txt"
        university_from_returned_dict = returned_education_job_map_dict["1"][0][2]

        xml = etree.parse(self.xml_file_directory + '/' + xml_file_name)
        university_from_xml = xml.xpath("//institution/text()")[0]

        assert_equals(university_from_returned_dict, university_from_xml)

    def test_degree_name_should_match_in_returned_dict_and_xml_file(self):
        returned_education_job_map_dict = extract_features_for_network_map(self.xml_file_directory, False)
        xml_file_name = "1.txt"
        degree_from_returned_dict = returned_education_job_map_dict["1"][0][4]

        xml = etree.parse(self.xml_file_directory + '/' + xml_file_name)
        degree_from_xml = xml.xpath("//degree/text()")[0]

        assert_equals(degree_from_returned_dict, degree_from_xml)

    def test_major_name_should_match_in_returned_dict_and_xml_file(self):
        returned_education_job_map_dict = extract_features_for_network_map(self.xml_file_directory, False)
        xml_file_name = "1.txt"
        major_from_returned_dict = returned_education_job_map_dict["1"][0][6]

        xml = etree.parse(self.xml_file_directory + '/' + xml_file_name)
        major_from_xml = xml.xpath("//major/text()")[0]

        assert_equals(major_from_returned_dict, major_from_xml)

    def test_major_code_should_match_in_returned_dict_and_xml_file(self):
        returned_education_job_map_dict = extract_features_for_network_map(self.xml_file_directory, False)
        xml_file_name = "1.txt"
        major_code_from_returned_dict = returned_education_job_map_dict["1"][0][5]

        xml = etree.parse(self.xml_file_directory + '/' + xml_file_name)
        major_code_from_xml = xml.xpath("//major/@code")[0]

        assert_equals(major_code_from_returned_dict, major_code_from_xml)

    def test_employer_name_should_match_in_returned_dict_and_xml_file(self):
        returned_education_job_map_dict = extract_features_for_network_map(self.xml_file_directory, False)
        xml_file_name = "1.txt"
        employer_from_returned_dict = returned_education_job_map_dict["1"][0][7]

        xml = etree.parse(self.xml_file_directory + '/' + xml_file_name)
        employer_from_xml = xml.xpath("//employer/text()")[0]

        assert_equals(employer_from_returned_dict, employer_from_xml)

    def test_job_title_should_match_in_returned_dict_and_xml_file(self):
        returned_education_job_map_dict = extract_features_for_network_map(self.xml_file_directory, False)
        xml_file_name = "1.txt"
        title_from_returned_dict = returned_education_job_map_dict["1"][0][10]

        xml = etree.parse(self.xml_file_directory + '/' + xml_file_name)
        title_from_xml = xml.xpath("//title/text()")[0]

        assert_equals(title_from_returned_dict, title_from_xml)


# t = TestNetworkMap()
# t.test_should_return_an_empty_dict_for_invalid_xml_directory()
# t.test_returned_education_job_map_dict_should_have_mapping_for_all_xml_resumes()
# t.test_university_name_should_match_in_returned_dict_and_xml_file()
# t.test_degree_name_should_match_in_returned_dict_and_xml_file()
# t.test_major_name_should_match_in_returned_dict_and_xml_file()
# t.test_major_code_should_match_in_returned_dict_and_xml_file()
# t.test_employer_name_should_match_in_returned_dict_and_xml_file()
# t.test_job_title_should_match_in_returned_dict_and_xml_file()
