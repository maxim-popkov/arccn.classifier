# -*- coding: utf-8 -*-
from django.db import models
# from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext as _

class Classifier(models.Model):

    """
    DataBase ORM Model for Classifier
    """
    title = models.CharField(max_length=64, verbose_name=u"Название")
    desc = models.TextField(verbose_name=u"Описание")
    save_file_path = models.CharField(max_length=64, null=True, blank=True, verbose_name=u"Путь к файлам")
    is_trained = models.BooleanField(default=False, verbose_name=u"Обучен?")

    class Meta:
        verbose_name = u'Классификатор'
        verbose_name_plural = u'Классификаторы'
        # verbose_title = u'Название'
        # verbose_save_file_path = u'Имя на диске'
        # verbose_is_trained = u'Обучен'

    def __unicode__(self):
        return self.title


class Label(models.Model):
    
    """
    DataBase ORM Model for Label
    """
    assigned_id = models.CharField(max_length=64, blank=True, verbose_name=u"клиентский id")    
    name = models.CharField(max_length=64, verbose_name=u"Название")
    cls = models.ForeignKey(Classifier, verbose_name=u"Классификатор")

    class Meta:
        verbose_name = u'Категория'
        verbose_name_plural = u'Категории'

    def __unicode__(self):
        return self.name


class TrainVector(models.Model):

    """
    DataBase ORM Model for Train Vector
    """
    assigned_id = models.CharField(max_length=64, blank=True, verbose_name=u"Клиентский id")
    cls = models.ForeignKey(Classifier, verbose_name=u"Классификатор")
    lbl = models.ForeignKey(Label, verbose_name=u"Категория")
    data = models.TextField(verbose_name=u"Термы")
    title = models.CharField(max_length=512, blank=True, verbose_name=u"Название")

    class Meta:
        verbose_name = u'Обучающий вектор'
        verbose_name_plural = u'Обучающие вектора'


    def __unicode__(self):
        return "Client UID: %s, Label: %s, Classifier: %s " %(self.assigned_id, self.lbl.name, self.cls.title)

    def __repr__(self):
        return "Client UID: %s, Label: %s, Classifier: %s " %(self.assigned_id, self.lbl.name, self.cls.title)


class TestVector(models.Model):
    
    """
    DataBase ORM Model for Test Vector
    """
    
    # param blank=True for admin panel,
    # with param can add vector without specifying foreignkeys
    assigned_id = models.CharField(max_length=64, blank=True, verbose_name=u"Клиентский id")
    cls = models.ForeignKey(
        Classifier, null=True, blank=True, db_constraint=False, verbose_name=u"Классификатор")
    lbl = models.ForeignKey(Label, null=True, blank=True, db_constraint=False, verbose_name=u"Категория")
    data = models.TextField(verbose_name=u"Термы")
    isClassified = models.BooleanField(default=False, verbose_name=u"Классифицирован?")
    accepted = models.BooleanField(default=False, verbose_name=u"Одобрен?")
    title = models.CharField(max_length=512, blank=True, verbose_name=u"Название")


    class Meta:
        verbose_name = u'Классифицируемый вектор'
        verbose_name_plural = u'Классифицируемые вектора'


    def __unicode__(self):
        return "Client UID: %s, Label: %s, Classifier: %s " %(self.assigned_id, self.lbl.name, self.cls.title)

    def __repr__(self):
        return "Client UID: %s, Label: %s, Classifier: %s " %(self.assigned_id, self.lbl.name, self.cls.title)
