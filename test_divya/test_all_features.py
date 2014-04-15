"""
Test to verify if all individual features extracted are combined coherently
"""

from nose.tools import eq_
from util import feature_consolidation
from lxml import etree

# Tests



def test_if_feature_consolidation_creates_list_of_features_of_length_4():
	dataxmllist = []
	dataxml = etree.parse('test_divya/samples/13.txt')
	dataxmllist.append((dataxml, 'software engineer', '13.txt'))
	uni = ['software','engineer']
	bi=['software engineer','University of','of California']

	result = feature_consolidation(dataxmllist,uni,bi)
	eq_(4,len(result[0]))


def test_if_feature_consolidation_creates_employers_names_length_3():
        dataxmllist = []
        dataxml = etree.parse('test_divya/samples/13.txt')
        dataxmllist.append((dataxml, 'software engineer', '13.txt'))
        uni = ['software','engineer']
        bi=['software engineer','University of','of California']

        result = feature_consolidation(dataxmllist,uni,bi)
        eq_(3,len(result[0][2]["employers"]))


def test_if_feature_consolidation_creates_recent_job_intern():
        dataxmllist = []
        dataxml = etree.parse('test_divya/samples/11.txt')
        dataxmllist.append((dataxml, 'software engineer', '13.txt'))
        uni = ['software','engineer']
        bi=['software engineer','University of','of California']

        result = feature_consolidation(dataxmllist,uni,bi)
        eq_('Intern',result[0][2]["jobs"][0])


def test_if_feature_consolidation_creates_degree_information_management():
        dataxmllist = []
        dataxml = etree.parse('test_divya/samples/13.txt')
        dataxmllist.append((dataxml, 'software engineer', '13.txt'))
        uni = ['software','engineer', 'intern']
        bi=['software engineer','University of','of California']

        result = feature_consolidation(dataxmllist,uni,bi)
        eq_('Master of Information Management and Systems',result[0][2]["degree"][0])

def test_if_feature_consolidation_creates_list_of_features_of_length_2_for_2_files():
        dataxmllist = []
        dataxml = etree.parse('test_divya/samples/13.txt')
	dataxml1 = etree.parse('test_divya/samples/11.txt')
        dataxmllist.append((dataxml, 'software engineer', '13.txt'))
 	dataxmllist.append((dataxml1,'researcher','11,txt'))
        uni = ['software','engineer','intern','java','c', 'responsible']
        bi=['software engineer','University of','of California']

        result = feature_consolidation(dataxmllist,uni,bi)
        eq_(2,len(result))	


