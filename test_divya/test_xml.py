"""
Test xml manipulation and feature extraction functionality 
"""

from nose.tools import eq_
from select_top_jobs import stripxml
from select_top_jobs import xml_features
from lxml import etree
# Tests

def test_gives_5_features_from_xml():
	xml_file = etree.parse("test_divya/samples/13.txt")
	features = xml_features(xml_file)
	eq_(5,len(features))

def test_institution_is_berkeley():
	xml_file = etree.parse("test_divya/samples/13.txt")
        features = xml_features(xml_file)
	eq_("University of California",features["institution"][0])

def test_degree_is_information_management():
	xml_file = etree.parse("test_divya/samples/13.txt")
        features = xml_features(xml_file)
	eq_("Master of Information Management and Systems",features["degree"][0])



def test_first_job_is_systems_engineer():
	xml_file = etree.parse("test_divya/samples/13.txt")
        features = xml_features(xml_file)
	eq_("Systems Engineer",features["jobs"][len(features["jobs"])-1])


def test_most_recent_job_is_vp():
	xml_file = etree.parse("test_divya/samples/13.txt")
        features = xml_features(xml_file)
	eq_("VP",features["jobs"][0])



def test_most_recent_employer_is_calcentral():
	xml_file = etree.parse("test_divya/samples/13.txt")
        features = xml_features(xml_file)
	eq_("CalCentral, University of California, Berkeley",features["employers"][0])

	
def test_jobs_employers_must_equal_3():
	xml_file = etree.parse("test_divya/samples/13.txt")
        features = xml_features(xml_file)
	eq_(3,len(features["employers"]))
	eq_(3,len(features["jobs"]))



