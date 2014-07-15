from app_classifier.models import Classifier, TrainVector, Label, TestVector
from rest_framework import serializers


class ClsSerializer(serializers.ModelSerializer):

    """Serializer class for Classifier model"""

    class Meta:
        model = Classifier
        fields = ('id', 'title', 'desc')
        read_only_fields = ('id',)


class VectorSerializer(serializers.ModelSerializer):

    """Serializer class for Train Vector model"""

    class Meta:
        model = TrainVector
        fields = ('id', 'assigned_id', 'data', 'cls', 'lbl')
        read_only_fields = ('id',)


class LabelSerializer(serializers.ModelSerializer):

    """Serializer class for Label model"""

    class Meta:
        model = Label
        fields = ('id', 'name', 'assigned_id', 'cls')
        read_only_fields = ('id',)


class TestVectorSerializer(serializers.ModelSerializer):

    """Serializer class for Test Vector model"""

    class Meta:
        model = TestVector
        fields = ('id', 'assigned_id','data', 'cls', 'lbl')
        read_only_fields = ('id','lbl')
