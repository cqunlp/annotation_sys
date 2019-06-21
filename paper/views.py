# -*- coding: utf-8 -*-
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from .models import *
from .forms import *
import time
import json
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import connections
import decimal
import datetime
from django.contrib.auth.decorators import login_required
from .serializers import *
from rest_framework import viewsets,filters
from django_filters.rest_framework import DjangoFilterBackend


# Create your views here.


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all().order_by('-id')
    serializer_class = SubjectSerialiser
    filterset_fields = ['id', 'name']
    search_fields = ['name']
    def get_queryset(self):
        user = self.request.user
        print(user)
        return Subject.objects.filter(id=1)

class DomainViewSet(viewsets.ModelViewSet):
    queryset = Domain.objects.all().order_by('-id')
    serializer_class = DomainSerialiser
    filterset_fields = ['id', 'name']
    search_fields = ['name']

class PaperViewSet(viewsets.ModelViewSet):
    queryset = Paper.objects.all().order_by('-id')
    serializer_class = PagerSerialiser
    filterset_fields = ['id', 'paper_title','keywords','subject','domain']
    search_fields = ['paper_title','keywords',]

class Paper_contentsViewSet(viewsets.ModelViewSet):
    queryset = Paper_contents.objects.all().order_by('-id')
    serializer_class = Paper_contentsSerialiser
    filterset_fields = ['id', 'parent','paper']
    search_fields = ['headline']

class ParagraphViewSet(viewsets.ModelViewSet):
    queryset = Paragraph.objects.all().order_by('-id')
    serializer_class = ParagraphSerialiser
    filterset_fields = ['id', 'paragraph_type','content']
    search_fields = ['paragraph_content']

