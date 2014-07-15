from service.models import Document, Text
from rest_framework import serializers

class DocSerializer(serializers.ModelSerializer):
	class Meta:
		model = Document
		fields = ('title', 'text', 'author')

class TxtSerializer(serializers.ModelSerializer):
	class Meta:
		model = Text
		fields = ['txt']

