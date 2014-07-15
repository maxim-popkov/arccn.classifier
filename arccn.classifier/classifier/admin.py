#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.contrib import admin
from django.conf import settings
from classifier.models import TestVector, TrainVector, Classifier, Label
import logging
import classify_master as cm
import classify_fabric as cf
import json
import os

def get_docs(db_vectors):
    """
    Get data from db_vectros to array docs
    """
    docs = []
    categories = []
    for vector in db_vectors:
        data = vector.data
        label = vector.lbl.assigned_id if vector.lbl else None
        doc = json.loads(data)
        docs.append(doc)
        categories.append(label)
    return docs, categories


def train_action(modeladmin, request, classifiers_set):
    """
    Train Classifier action
    """
    if not classifiers_set:
        return

    for db_clf in classifiers_set:
        # TrainVector.objects.all()
        raw_train_vectors = db_clf.trainvector_set.all()
        title = db_clf.title
        train_docs, train_labels = get_docs(raw_train_vectors)

        clf = cf.Classifier()
        train_set = clf.weight_train_vectors(train_docs)
        clf.train(train_set, train_labels)
        
        db_clf.is_trained = True
        db_clf.save_file_path = settings.MEDIA_ROOT 
        db_clf.save()
        clf.save_on_disk(settings.MEDIA_ROOT, title)
        
    logging.info('TRAIN COMPLETE')

class prettyfloat(float):
    def __repr__(self):
        return "%0.2f" % self

def classify_action(modeladmin, request, classifiers_set):
    """
    Classify admin action
    """
    if not classifiers_set:
        return

    for db_clf in classifiers_set:
        raw_test_vectors = db_clf.testvector_set.all()
        title = db_clf.title
        test_docs, _ = get_docs(raw_test_vectors)
        clf = cf.Classifier(settings.MEDIA_ROOT, 'clf_name')    

#    logging.info(test_docs)
        test_set = clf.weight_test_vectors(test_docs)
        predict_labels = clf.predict(test_set)
        predict_probs = clf.predict_probs(test_set)
        pretty_probs = []
        for probs in predict_probs:
            pretty_probs.append(map(prettyfloat, probs))
        logging.info('========================')
        logging.info(predict_labels)
        logging.info(pretty_probs)

        classified_pairs = zip(raw_test_vectors, predict_labels)

        for db_test_vector, label in classified_pairs:
            db_predicted_label = Label.objects.filter(assigned_id=label)[0]
            db_test_vector.lbl = db_predicted_label
            db_test_vector.isClassified = True
            db_test_vector.save()


class TestVectorAdmin(admin.ModelAdmin):
    list_display = ['_assigned_id', '_isClassified', '_cls', '_lbl']
    list_filter = ('isClassified', 'cls', 'lbl')
    
    def _assigned_id(self, obj):
        return obj.assigned_id

    def _cls(self, obj):
        return obj.cls

    def _lbl(self, obj):
        return obj.lbl

    def _isClassified(self, obj):
        return obj.isClassified

    _assigned_id.short_description = 'Идентификатор клиента'
    _cls.short_description = 'Классификатор'
    _lbl.short_description = 'Категория'
    _isClassified.short_description = 'Статус Классификации'
    _isClassified.boolean = True

class LabelInline(admin.TabularInline):
    model = Label
    extra = 1

class LabelAdmin(admin.ModelAdmin):
    list_display = ['name', 'assigned_id', 'id']

class TrainVectorAdmin(admin.ModelAdmin):
    list_display = ['assigned_id', 'lbl', 'cls']
    list_filter = ('cls', 'lbl')

class ClassifierAdmin(admin.ModelAdmin):
    readonly_fields = ('no_wait_for_test',)
    list_display = ['title', 'is_trained', 'desc', 'id', 'no_wait_for_test']
    actions = [train_action, classify_action]
    list_filter = ['title']
    inlines = [LabelInline]

    def no_wait_for_test(self, db_clf):
        return not db_clf.testvector_set.filter(lbl=None) 

    no_wait_for_test.boolean = True
    no_wait_for_test.short_description = u'Статус классифиции'

classify_action.short_description = u'Классифицировать документы'
train_action.short_description = u'Обучить классификатор'

admin.site.register(TestVector, TestVectorAdmin)
admin.site.register(TrainVector, TrainVectorAdmin)
admin.site.register(Classifier, ClassifierAdmin)
admin.site.register(Label, LabelAdmin)
