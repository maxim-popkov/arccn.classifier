from django.contrib import admin
from django.conf import settings
from classifier.models import TestVector, TrainVector, Classifier, Label
import logging
import classify_master as cm
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

    for cl in classifiers_set:
        # TrainVector.objects.all()
        raw_train_vectors = cl.trainvector_set.all()
        train_docs, train_labels = get_docs(raw_train_vectors)
        train_set = cm.weight_train_vectors(train_docs)
        cm.train(train_set, train_labels)
        cl.is_trained = True
        cl.save_file_path = settings.MEDIA_ROOT 
        cm.save_on_disk(settings.MEDIA_ROOT, 'clf_name')
        cl.save()
    logging.info('TRAIN COMPLETE')

class prettyfloat(float):
    def __repr__(self):
        return "%0.2f" % self

def classify_action(modeladmin, request, queryset):
    """
    Classify admin action
    """
    if not queryset:
        return
    clf = cm.load_from_disk(settings.MEDIA_ROOT, 'clf_name')

    raw_test_vectors = TestVector.objects.all()
    test_docs, tmp = get_docs(raw_test_vectors)

    logging.info(test_docs)
    test_set = cm.weight_test_vectors(clf['dvt'], clf['tft'], test_docs)
    predict_labels = cm.predict(clf['clf'], test_set)
    predict_probs = cm.predict_probs(clf['clf'], test_set)
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
    list_display = ['_assigned_id', 'isClassified', '_cls', '_lbl']
    list_filter = ('isClassified', 'cls', 'lbl')
    actions = [classify_action]

    def _assigned_id(self, obj):
        return obj.assigned_id

    def _cls(self, obj):
        return obj.cls

    def _lbl(self, obj):
        return obj.lbl

    _assigned_id.short_description = 'Assigned Name'
    _cls.short_description = 'Classifier'
    _lbl.short_description = 'Label'

class LabelInline(admin.TabularInline):
    model = Label
    extra = 1

class LabelAdmin(admin.ModelAdmin):
    list_display = ['name', 'assigned_id', 'id']

class TrainVectorAdmin(admin.ModelAdmin):
    list_display = ['assigned_id', 'lbl', 'cls']
    list_filter = ('cls', 'lbl')
    actions = [train_action]


class ClassifierAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_trained', 'desc', 'id']
    actions = [train_action]
    inlines = [LabelInline]

classify_action.short_description = "Classify selected objects"
train_action.short_description = 'Train selected objects'

admin.site.register(TestVector, TestVectorAdmin)
admin.site.register(TrainVector, TrainVectorAdmin)
admin.site.register(Classifier, ClassifierAdmin)
admin.site.register(Label, LabelAdmin)
