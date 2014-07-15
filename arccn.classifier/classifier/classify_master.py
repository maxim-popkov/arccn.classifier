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

logging.info("INIT START")
dict_vectorizer = DictVectorizer()
tfidf_transformer = TfidfTransformer()
clf = MultinomialNB(alpha=.01)

classifier_parts = {\
                    'clf':'classify_master.clf',\
                    'dvt':'dict_vectorizer.dvt',\
                    'tft':'tfidf_transformer.tft'\
                    }

def weight_train_vectors(vectors):
    """
    Weight train feature vectors
    """
    sparse_matrix = dict_vectorizer.fit_transform(vectors)
    sparse_tf_idf = tfidf_transformer.fit_transform(sparse_matrix)

    return sparse_tf_idf


def weight_test_vectors(dict_vectorizer, tfidf_transformer, vectors):
    """
    Weight test feature vectors
    """
    logging.info("TEST WEIGHT START")
    logging.info(dict_vectorizer.vocabulary_)
    sparse_matrix = dict_vectorizer.transform(vectors)
    logging.info("DICT COMPLETE")
    sparse_tf_idf = tfidf_transformer.transform(sparse_matrix)
    logging.info("TEST WEIGHT END")
    return sparse_tf_idf


def train(train_set, categories):
    """
    Train Classifier on feature vectors
    in: sparse matrix, labels sequence
    """
    clf.fit(train_set, categories)

def predict(clf, test_set):
    """
    Predict results
    in: sparse matrix
    """
    logging.info("PREDICT")
    pred = clf.predict(test_set)
    return pred

def predict_probs(clf, test_set):
    """
    Predict probabilities results
    in: sparse matrix
    """
    logging.info("PREDICT PROBS")
    probs = clf.predict_proba(test_set)
    return probs

def save_on_disk(directory, clf_name = None):
    """
    Save Classifier on Disk
    """
    clf_filename = os.path.join(directory, classifier_parts['clf'])
    dvt_filename = os.path.join(directory, classifier_parts['dvt'])
    tft_filename = os.path.join(directory, classifier_parts['tft'])

    joblib.dump(clf, clf_filename, compress=9)
    joblib.dump(dict_vectorizer, dvt_filename, compress=9)
    joblib.dump(tfidf_transformer, tft_filename, compress=9)

def load_from_disk(directory, clf_name = None):
    """
    Load Classifier from disk
    """
    logging.info("LOAD CLASSIFIER")
    clf_filename = os.path.join(directory, classifier_parts['clf'])
    dvt_filename = os.path.join(directory, classifier_parts['dvt'])
    tft_filename = os.path.join(directory, classifier_parts['tft'])

    clf = joblib.load(clf_filename)
    dict_vectorizer = joblib.load(dvt_filename)
    tfidf_transformer = joblib.load(tft_filename)
    return {'clf':clf, 'dvt':dict_vectorizer, 'tft':tfidf_transformer}
