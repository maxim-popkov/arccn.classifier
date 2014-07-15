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
import logging
import os

class Classifier(object):
    """docstring for Classifier"""
    def __init__(self, directory=None, clf_name=None):
        
        self._clf = None
        self._dvt = None
        self._tft = None

        logging.info("INIT START")
        if directory and clf_name:
            self.load_from_disk(directory, clf_name)
        else:
            self._clf = MultinomialNB(alpha=.01)
            self._dvt = DictVectorizer()
            self._tft = TfidfTransformer()
        
    def weight_train_vectors(self, vectors):
        """
        Weight train feature vectors
        """
        dict_vectorizer = self._dvt
        tfidf_transformer = self._tft

        sparse_matrix = dict_vectorizer.fit_transform(vectors)
        sparse_tf_idf = tfidf_transformer.fit_transform(sparse_matrix)
        return sparse_tf_idf

    def weight_test_vectors(self, vectors):
        """
        Weight test feature vectors
        """
        dict_vectorizer = self._dvt
        tfidf_transformer = self._tft
        
        logging.info("TEST WEIGHT START")
        logging.info(dict_vectorizer.vocabulary_)
        sparse_matrix = dict_vectorizer.transform(vectors)
        logging.info("DICT COMPLETE")
        sparse_tf_idf = tfidf_transformer.transform(sparse_matrix)
        logging.info("TEST WEIGHT END")
        return sparse_tf_idf

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
    
    def save_on_disk(self, directory, clf_name):
        """
        Save Classifier on Disk
        """
        clf_filename = os.path.join(directory, clf_name + '.clf')
        dvt_filename = os.path.join(directory, clf_name + '.dvt')
        tft_filename = os.path.join(directory, clf_name + '.tft')

        joblib.dump(self._clf, clf_filename, compress=9)
        joblib.dump(self._dvt, dvt_filename, compress=9)
        joblib.dump(self._tft, tft_filename, compress=9)

    def load_from_disk(self, directory, clf_name):
        """
        Load Classifier from disk
        """
        logging.info("LOAD CLASSIFIER")
        clf_filename = os.path.join(directory, clf_name + '.clf')
        dvt_filename = os.path.join(directory, clf_name + '.dvt')
        tft_filename = os.path.join(directory, clf_name + '.tft')

        self._clf = joblib.load(clf_filename)
        self._dvt = joblib.load(dvt_filename)
        self._tft = joblib.load(tft_filename)