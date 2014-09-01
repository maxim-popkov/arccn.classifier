#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.contrib import admin
from django.conf import settings
from django.forms import TextInput
from django.db import models
from app_classifier.models import TestVector, TrainVector, Classifier, Label
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
    titles = []
    categories = []
    for vector in db_vectors:
        data = vector.data
        title = vector.title
        label = vector.lbl.assigned_id if vector.lbl else None
        doc = json.loads(data)
        docs.append(doc)
        titles.append(title)
        categories.append(label)
    return docs, titles, categories


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
        train_docs, train_titles, train_labels = get_docs(raw_train_vectors)

        clf = cf.Classifier()
        train_docs = clf.term_cleaner(train_docs)
        train_pages_set = clf.weight_train_pages(train_docs)
        logging.info('Pages trained')
        logging.info(train_titles)
        train_names_set = clf.weight_train_names(train_titles)
        logging.info('Names trained')
        train_set = clf.concatenate(train_pages_set, train_names_set)
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
        raw_test_vectors = db_clf.testvector_set.filter(accepted=False)
        title = db_clf.title
        test_docs, test_titles, _ = get_docs(raw_test_vectors)
        clf = cf.Classifier(settings.MEDIA_ROOT, title)    

#    logging.info(test_docs)
        test_pages_set = clf.weight_test_pages(test_docs)
        test_names_set = clf.weight_test_names(test_titles)
        test_set = clf.concatenate(test_pages_set, test_names_set)
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

def accept_action(modeladmin, request, vectors_set):
    """
    Set flag accepted in admin interface
    """
    if not vectors_set:
        return
    for vector in vectors_set:
        vector.accepted = True
        vector.save()

class TestVectorAdmin(admin.ModelAdmin):
    actions = [accept_action]
    list_display = ['_assigned_id', '_title', '_isClassified', 'accepted','_cls', '_lbl']
    list_filter = ('isClassified', 'cls', 'lbl')
    search_fields = ('title',)
    
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'20'})},
    }

    def _title(self, obj):
        return obj.title

    def _assigned_id(self, obj):
        return obj.assigned_id

    def _cls(self, obj):
        return obj.cls

    def _lbl(self, obj):
        return obj.lbl

    def _isClassified(self, obj):
        return obj.isClassified

    _title.short_description = u'Название документа'
    _assigned_id.short_description = u'Идентификатор клиента'
    _cls.short_description = u'Классификатор'
    _lbl.short_description = u'Категория'
    _isClassified.short_description = u'Статус Классификации'
    _isClassified.boolean = True

accept_action.short_description = u'Одобрить выбранные'

class LabelInline(admin.TabularInline):
    model = Label
    extra = 1

class LabelAdmin(admin.ModelAdmin):
    list_display = ['name', 'assigned_id', 'id']

class TrainVectorAdmin(admin.ModelAdmin):
    list_display = ['_assigned_id', '_title', '_lbl', '_cls']
    list_filter = ('cls', 'lbl')

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'20'})},
    }

    def _title(self, obj):
        return obj.title

    def _assigned_id(self, obj):
        return obj.assigned_id

    def _cls(self, obj):
        return obj.cls

    def _lbl(self, obj):
        return obj.lbl

    def _isClassified(self, obj):
        return obj.isClassified

    _title.short_description = 'Название документа'
    _assigned_id.short_description = 'Идентификатор клиента'
    _cls.short_description = 'Классификатор'
    _lbl.short_description = 'Категория'
    _isClassified.short_description = 'Статус Классификации'
    _isClassified.boolean = True


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
