import string
import numpy as np
import scipy.sparse as sp
import marisa_trie
# import datrie
# import chartrie

from sklearn.externals import six
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, _make_int_array


# hack to store vocabulary in MARISA Trie
class _MarisaVocabularyMixin(object):
    def fit_transform(self, raw_documents, y=None):
        super(_MarisaVocabularyMixin, self).fit_transform(raw_documents)
        self._freeze_vocabulary()
        return super(_MarisaVocabularyMixin, self).fit_transform(raw_documents, y)

    def _freeze_vocabulary(self):
        if not self.fixed_vocabulary:
            self.vocabulary_ = marisa_trie.Trie(self.vocabulary_.keys())
            self.fixed_vocabulary = True
            del self.stop_words_


class MarisaCountVectorizerOld(_MarisaVocabularyMixin, CountVectorizer):
    pass


class ReducedCountVectorizer(CountVectorizer):
    def _sort_features(self, X, vocabulary):
        return X

    def _limit_features(self, X, vocabulary, high=None, low=None,
                        limit=None):
        return X, set()


class _TrieCountVectorizer(ReducedCountVectorizer):
    trie_cls = None

    def _count_vocab(self, raw_documents, fixed_vocab):
        """Create sparse feature matrix, and vocabulary where fixed_vocab=False
        """
        if fixed_vocab:
            raise NotImplementedError()

        vocabulary = self.trie_cls()

        analyze = self.build_analyzer()
        j_indices = _make_int_array()
        indptr = _make_int_array()
        indptr.append(0)
        for doc in raw_documents:
            for feature in analyze(doc):
                if feature not in vocabulary:
                    idx = len(vocabulary)
                    vocabulary[feature] = idx
                    j_indices.append(idx)
                else:
                    try:
                        j_indices.append(vocabulary[feature])
                    except KeyError:
                        # Ignore out-of-vocabulary items for fixed_vocab=True
                        continue
            indptr.append(len(j_indices))

        # some Python/Scipy versions won't accept an array.array:
        if j_indices:
            j_indices = np.frombuffer(j_indices, dtype=np.intc)
        else:
            j_indices = np.array([], dtype=np.int32)
        indptr = np.frombuffer(indptr, dtype=np.intc)
        values = np.ones(len(j_indices))

        X = sp.csr_matrix((values, j_indices, indptr),
                          shape=(len(indptr) - 1, len(vocabulary)),
                          dtype=self.dtype)
        X.sum_duplicates()
        return vocabulary, X

    def _sort_features(self, X, vocabulary):
        return X

    def _limit_features(self, X, vocabulary, high=None, low=None,
                        limit=None):
        return X, set()


# class DatrieCountVectorizer(_TrieCountVectorizer):  # it segfaults
#     trie_cls = lambda *args: datrie.Trie(ranges=[(chr(1), chr(255))])

# class ChartrieCountVectorizer(_TrieCountVectorizer):  # can't get it work
#     trie_cls = chartrie.CharTrie


class MarisaCountVectorizer(CountVectorizer):

    # ``CountVectorizer.fit`` method calls ``fit_transform`` so
    # ``fit`` is not provided
    def fit_transform(self, raw_documents, y=None):
        X = super(MarisaCountVectorizer, self).fit_transform(raw_documents)
        X = self._freeze_vocabulary(X)
        return X

    def _freeze_vocabulary(self, X=None):
        if not self.fixed_vocabulary:
            frozen = marisa_trie.Trie(six.iterkeys(self.vocabulary_))
            if X is not None:
                X = self._reorder_features(X, self.vocabulary_, frozen)
            self.vocabulary_ = frozen
            self.fixed_vocabulary = True
            del self.stop_words_
        return X

    def _reorder_features(self, X, old_vocabulary, new_vocabulary):
        map_index = np.empty(len(old_vocabulary), dtype=np.int32)
        for term, new_val in six.iteritems(new_vocabulary):
            map_index[new_val] = old_vocabulary[term]
        return X[:, map_index]


class MarisaTfidfVectorizer(TfidfVectorizer):

    def fit_transform(self, raw_documents, y=None):
        super(MarisaTfidfVectorizer, self).fit_transform(raw_documents)
        self._freeze_vocabulary()
        return super(MarisaTfidfVectorizer, self).fit_transform(raw_documents, y)

    def fit(self, raw_documents, y=None):
        super(MarisaTfidfVectorizer, self).fit(raw_documents)
        self._freeze_vocabulary()
        return super(MarisaTfidfVectorizer, self).fit(raw_documents, y)

    def _freeze_vocabulary(self, X=None):
        if not self.fixed_vocabulary:
            self.vocabulary_ = marisa_trie.Trie(six.iterkeys(self.vocabulary_))
            self.fixed_vocabulary = True
            del self.stop_words_
