from app_classifier.models import Classifier, TrainVector, Label
from app_classifier.serializers import ClsSerializer, VectorSerializer, LabelSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)


class VectorList(APIView):

    """
    List all Train Vectors, or create a new Train Vector.
    """

    def get(self, request, cls_id, format=None):
        vectors = TrainVector.objects.all()
        serializer = VectorSerializer(vectors, many=True)
        return Response(serializer.data)

    def post(self, request, cls_id, format=None):
        serializer = VectorSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LabelList(APIView):

    """
    List all Labels, or create a new Label.
    """

    def get(self, request, cls_id, format=None):
        lbls = Label.objects.all()
        serializer = LabelSerializer(lbls, many=True)
        return Response(serializer.data)

    def post(self, request, cls_id, format=None):
        serializer = LabelSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClsList(APIView):

    """
    List all Classifiers, or create a new Classifier.
    """

    def get(self, request, format=None):
        classifiers = Classifier.objects.all()
        serializer = ClsSerializer(classifiers, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ClsSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClsDetail(APIView):

    """
    Retrieve, update or delete a Classifier Details.
    """

    def get_object(self, cls_id):
        try:
            return Classifier.objects.get(pk=cls_id)
        except Classifier.DoesNotExist:
            raise Http404

    def get(self, request, cls_id, format=None):
        cls = self.get_object(cls_id)
        serializer = ClsSerializer(cls)
        return Response(serializer.data)

    def put(self, request, cls_id, format=None):
        cls = self.get_object(cls_id)
        serializer = ClsSerializer(cls, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, cls_id, format=None):
        cls = self.get_object(cls_id)
        cls.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
