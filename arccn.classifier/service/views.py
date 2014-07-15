from django.shortcuts import render
from django.http import HttpResponse

from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response

from service.models import Document, Text
from service.serializers import DocSerializer, TxtSerializer

# class JSONResponse(HttpResponse):
#     """
#     An HttpResponse that renders its content into JSON.
#     """
#     def __init__(self, data, **kwargs):
#         content = JSONRenderer().render(data)
#         kwargs['content_type'] = 'application/json'
#         super(JSONResponse, self).__init__(content, **kwargs)

# Create your views here.
# 
@api_view(['GET', 'POST'])
def doc_list(request):
    """
    List all code docs, or create a new snippet.
    """
    if request.method == 'GET':
        docs = Document.objects.all()
        serializer = DocSerializer(docs, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.DATA #JSONParser().parse(request)
        serializer = DocSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def txt_list(request, pk):
    """
    List all code txts, or create a new txt.
    """
    if request.method == 'GET':
        txts = Text.objects.all()
        serializer = TxtSerializer(txts, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.DATA #JSONParser().parse(request)
        serializer = TxtSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        

@api_view(['GET', 'PUT', 'DELETE'])
def doc_detail(request, pk):
    """
    Retrieve, update or delete a code doc.
    """
    try:
        doc = Document.objects.get(pk=pk)
    except Document.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = DocSerializer(doc)
        return Response(serializer.data)

    elif request.method == 'PUT':
        data = request.DATA
        serializer = DocSerializer(doc, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        doc.delete()
        return HttpResponse(status=204)