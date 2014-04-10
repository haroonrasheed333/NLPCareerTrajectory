"""
Verify job title normalization functionality
"""

from nose.tools import *
from JobTitleNormalization import normalize_job_titles

# Tests


def test_should_normalize_different_permutations_of_same_job_titles():
    original_titles = \
        [
            "director of finance",
            "Director of Finance",
            "DIRECTOR OF FINANCE",
            "finance director",
            "Finance Director",
            "FINANCE DIRECTOR",
        ]
    expected_normalized_title = "director of finance"

    normalized_titles = normalize_job_titles(original_titles)

    for normalized_title in normalized_titles:
        assert_equals(expected_normalized_title, normalized_title)


def test_should_expand_job_titles():
    original_titles = \
        [
            "sr project mgr",
            "sr project mgr.",
            "sr project mngr",
            "sr project mngr.",
            "sr. project mgr",
            "sr. project mgr.",
            "sr. project mngr",
            "sr. project mngr.",
        ]
    expected_normalized_title = "senior project manager"

    normalized_titles = normalize_job_titles(original_titles)

    for normalized_title in normalized_titles:
        assert_equals(expected_normalized_title, normalized_title)