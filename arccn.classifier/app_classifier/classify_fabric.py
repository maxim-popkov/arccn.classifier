#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
======================================================
Classifier for features
======================================================
"""
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.externals import joblib

from collections import Counter
import numpy as np
import copy
import logging
import os

class Classifier(object):
    """docstring for Classifier"""
    def __init__(self, directory=None, clf_name=None):
        
        self._clf = None
        self._dvt_pages = None
        self._tft_pages = None
        self._tvt_names = None

        logging.info("INIT START")
        if directory and clf_name:
            self.load_from_disk(directory, clf_name)
        else:
            self._clf = MultinomialNB(alpha=.01)
            self._dvt_pages = DictVectorizer()
            self._tft_pages = TfidfTransformer()
            self._tvt_names = TfidfVectorizer(use_idf=True)
    
    def term_cleaner(self, vectors):
        """
        Remove bad Digits from pages
        Use Before Train Step
        """
        cleaned_vectors = copy.copy(vectors)

        import string
        dict_vectorizer = DictVectorizer()
        
        dict_vectorizer.fit(cleaned_vectors)
        terms = dict_vectorizer.vocabulary_.keys()
        bad_terms = [term for term in terms if term[0] in string.digits or len(term) <= 2]
        
        for vector in cleaned_vectors:
            old_len = len(vector)
            for term in bad_terms:
                if vector.has_key(term): vector.pop(term)
            new_len = len(vector)
            print(old_len, new_len)
        
        return cleaned_vectors

    def weight_train_pages(self, vectors):
        """
        Weight train feature pages
        """
        dict_vectorizer = self._dvt_pages
        tfidf_transformer = self._tft_pages

        sparse_matrix = dict_vectorizer.fit_transform(vectors)
        sparse_tf_idf = tfidf_transformer.fit_transform(sparse_matrix)
        return sparse_tf_idf

    def weight_train_names(self, vectors):
        """
        Weight train names
        Return spatse matrix with weights
        """
        vect_names = self._tvt_names
        sparse_names = vect_names.fit_transform(vectors)
        return sparse_names

    def weight_test_pages(self, vectors):
        """
        Weight test feature vectors
        """
        dict_vectorizer = self._dvt_pages
        tfidf_transformer = self._tft_pages
        
        logging.info("TEST WEIGHT START")
        logging.info(dict_vectorizer.vocabulary_)
        sparse_matrix = dict_vectorizer.transform(vectors)
        logging.info("DICT COMPLETE")
        sparse_tf_idf = tfidf_transformer.transform(sparse_matrix)
        logging.info("TEST WEIGHT END")
        return sparse_tf_idf

    def weight_test_names(self, vectors):
        """
        Weight test names
        Return spatse matrix with weights
        """
        vect_names = self._tvt_names
        sparse_names = vect_names.transform(vectors)

        return sparse_names

    def train(self, train_set, categories):
        """
        Train Classifier on feature vectors
        in: sparse matrix, labels sequence
        """
        self._clf.fit(train_set, categories)

    def predict(self, test_set):
        """
        Predict results
        in: sparse matrix
        """
        logging.info("PREDICT")
        pred = self._clf.predict(test_set)
        return pred

    def predict_probs(self, test_set):
        """
        Predict probabilities results
        in: sparse matrix
        """
        logging.info("PREDICT PROBS")
        probs = self._clf.predict_proba(test_set)
        return probs

    def concatenate(self, sparse_pages, sparse_names):
        X1 = sparse_pages.todense()
        X2 = sparse_names.todense()
        return np.concatenate((X1,X2), axis=1)
    
    def save_on_disk(self, directory, clf_name):
        """
        Save Classifier on Disk
        """
        clf_filename = os.path.join(directory, clf_name + '.clf')
        dvt_pages_filename = os.path.join(directory, clf_name + '_pages.dvt')
        tvt_names_filename = os.path.join(directory, clf_name + '_names.tvt')
        tft_pages_filename = os.path.join(directory, clf_name + '_pages.tft')


        joblib.dump(self._clf, clf_filename, compress=9)
        joblib.dump(self._dvt_pages, dvt_pages_filename, compress=9)
        joblib.dump(self._tvt_names, tvt_names_filename, compress=9)
        joblib.dump(self._tft_pages, tft_pages_filename, compress=9)

    def load_from_disk(self, directory, clf_name):
        """
        Load Classifier from disk
        """
        logging.info("LOAD CLASSIFIER")
        clf_filename = os.path.join(directory, clf_name + '.clf')
        dvt_pages_filename = os.path.join(directory, clf_name + '_pages.dvt')
        tvt_names_filename = os.path.join(directory, clf_name + '_names.tvt')
        tft_pages_filename = os.path.join(directory, clf_name + '_pages.tft')

        self._clf = joblib.load(clf_filename)
        self._dvt_pages = joblib.load(dvt_pages_filename)
        self._tvt_names = joblib.load(tvt_names_filename)
        self._tft_pages = joblib.load(tft_pages_filename)