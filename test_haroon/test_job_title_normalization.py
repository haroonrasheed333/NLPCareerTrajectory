"""
Verify job title normalization functionality
"""

from nose.tools import *
from JobTitleNormalization import normalize_job_titles, expand_job_title, title_permutations

# Tests


def test_ceo_should_be_expanded_as_chief_executive_officer():
    actual_title = "ceo"
    expected_title = "chief executive officer"
    expanded_title = expand_job_title(actual_title)
    assert_equals(expanded_title, expected_title)


def test_software_developer_should_be_normalized_as_software_engineer():
    actual_title = ["software developer"]
    expected_title = ["software engineer"]
    normalized_title = normalize_job_titles(actual_title)
    assert_equals(normalized_title, expected_title)


def test_different_variants_of_same_title_should_be_properly_normalized():
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


def test_different_permutations_of_same_title_should_be_properly_normalized():
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


def test_actual_titles_list_and_normalized_titles_list_should_be_of_same_length():
    actual_titles = ["software developer", "ceo", "business analyst", "vp"]
    normalized_titles = normalize_job_titles(actual_titles)

    assert_equals(len(actual_titles), len(normalized_titles))