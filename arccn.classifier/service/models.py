from django.db import models
# Create your models here.

class Document(models.Model):
	title = models.CharField(max_length=64)
	text = models.TextField()
	author = models.CharField(max_length=64)

class Text(models.Model):
	"""docstring for Text"""
	txt = models.TextField(max_length=64)	
