from app_classifier.models import TestVector
from app_classifier.serializers import TestVectorSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)


class ClassifyList(APIView):

    """
    List all snippets, or create a new snippet.
    """

    def get(self, request, cls_id, format=None):
        vectors = TestVector.objects.all()
        serializer = TestVectorSerializer(vectors, many=True)
        return Response(serializer.data)

    def post(self, request, cls_id, format=None):
        serializer = TestVectorSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
