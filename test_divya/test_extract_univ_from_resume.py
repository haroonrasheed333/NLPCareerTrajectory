"""
Test to verify if all individual features extracted are combined coherently
"""

from nose.tools import eq_
from univ_lookup import extract_from_resume
from util import stripxml

# Tests

test_reume =""
def test_if_resume_split_at_word_education():
