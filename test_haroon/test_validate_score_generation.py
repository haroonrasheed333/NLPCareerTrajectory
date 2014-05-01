"""
Validate score generation functionality
"""
from nose.tools import *
from util2 import get_top_five_predictions


class TestScoreGeneration():
    def __init__(self):
        self.predicted_decisions = [[-0.432, -0.523, -0.333, -0.621, -0.854, -0.443, -0.356, -0.999, -0.764]]
        self.labels = \
            [
                "Consultant", "Project Manager", "Data Analyst", "Product Manager", "Chief Executive Officer",
                "Software Engineer", "Senior Software Engineer", "Customer Service Representative", "Graphic Designer"
            ]


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

    def test_should_return_top_five_predicted_titles(self):
        top_five_predictions, normalized_scores = get_top_five_predictions(self.predicted_decisions, self.labels)
        assert_equal(5, len(top_five_predictions))

    def test_top_predicted_title_should_be_data_analyst(self):
        top_five_predictions, normalized_scores = get_top_five_predictions(self.predicted_decisions, self.labels)
        assert_equals("Data Analyst", top_five_predictions[0])

    def test_highest_normalized_score_should_be_hundred(self):
        top_five_predictions, normalized_scores = get_top_five_predictions(self.predicted_decisions, self.labels)
        assert_equals(100, normalized_scores[0])

    def test_lowest_normalized_score_should_be_greater_than_or_equal_to_zero(self):
        top_five_predictions, normalized_scores = get_top_five_predictions(self.predicted_decisions, self.labels)
        assert_greater_equal(normalized_scores[len(normalized_scores) - 1], 0)

    def test_should_return_empty_lists_when_valid_decision_list_is_not_passed(self):
        top_five_predictions, normalized_scores = get_top_five_predictions([], [])
        assert_equals([], top_five_predictions)
        assert_equals([], normalized_scores)


# t = TestScoreGeneration()
# t.setup_class()
# t.test_should_return_top_five_predicted_titles()
# t.test_top_predicted_title_should_be_data_analyst()
# t.test_highest_normalized_score_should_be_hundred()
# t.test_lowest_normalized_score_should_be_greater_than_or_equal_to_zero()
# t.test_should_return_empty_lists_when_valid_decision_list_is_not_passed()
# t.teardown_class()