"""
Test functionality to generate files for creating network graph
"""

from nose.tools import eq_
from univ_lookup import create_data
import json
skills_employer = json.loads(open("static/networkgraphtest.json").read())
univ_major_number = json.loads(open("static/univ_mapping.json").read())

def test_ucb_must_generate_data():
    univ = "university of california berkeley"
    result = create_data(univ, skills_employer, univ_major_number)
    if (result["links"]):
        value = True
    eq_(True, value)

def test_ucb_must_generate_15_links():
    univ = "university of california berkeley"
    result = create_data(univ, skills_employer, univ_major_number)
    eq_(126, len(result["links"]))

def test_ucb_must_include_the_population_council_as_first_result():
    univ = "university of california berkeley"
    result = create_data(univ, skills_employer, univ_major_number)
    if (result["links"][0]["source"] == "The Population Council"):
        value = True
    eq_(True, value)

def test_ucb_must_include_word_as_first_result_value():
    univ = "university of california berkeley"
    result = create_data(univ, skills_employer, univ_major_number)
    if (result["links"][0]["target"] == "word"):
        value = True
    eq_(True, value)

def test_ucb_must_have_source_and_target_for_each_term():
    univ = "university of california berkeley"
    result = create_data(univ, skills_employer, univ_major_number)
    value = 0
    for link in result["links"]:
        if (link["source"]):
            if(link["target"]):
                value = value+1
    eq_(126, value)

def test_must_retusn_links_with_source_and_target():
    univ = "university of california berkeley"
    result = create_data(univ, skills_employer, univ_major_number)
    value = True
    for link in result["links"]:
        if "source" not in link:
            if "target" not in link:
                value = False
    eq_(True, value)