from nose.tools import eq_
from career_trajectory_svm_new import unigram_features

def test_should_generate_unigrams_from_text_and_create_feature_set():
  test_text = "Responsible for implementing high level security features successfully"
  unigram_list =['responsible', 'developed', 'monitored', 'solution']
  unigram_feature = unigram_features(test_text,unigram_list)
  expected_value=4
  eq_(expected_value,len(unigram_feature))

def test_should_stem_words_and_create_feature_set():
  test_text = "Responsible for developing and implementing high level security features successfully"
  unigram_list =['responsible', 'develop', 'implement', 'success']
  unigram_feature = unigram_features(test_text,unigram_list)
  expected_value=1
  eq_(expected_value,unigram_feature[0])
  eq_(expected_value,unigram_feature[1])
  eq_(expected_value,unigram_feature[2])
  eq_(expected_value,unigram_feature[3])

def test_should_append_zero_if_unigram_is_not_present_in_text():
  test_text = "Responsible for developing and implementing high level security features successfully. Led a team of 10 people and pushed a new enhancement in 4 weeks without any bugs"
  unigram_list =['responsible', 'developed', 'monitored', 'solution', 'java', 'c++', 'strong']
  unigram_feature = unigram_features(test_text,unigram_list)
  eq_(0,unigram_feature[3])
  eq_(0,unigram_feature[4])
  eq_(0,unigram_feature[5])
  eq_(0,unigram_feature[6])
