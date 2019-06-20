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
    filter_backends = (filters.SearchFilter,DjangoFilterBackend)
    filterset_fields = ('id', 'name')
    search_fields = ('name')
    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        print(user)
        return Subject.objects.all()
class DomainViewSet(viewsets.ModelViewSet):
    queryset = Domain.objects.all().order_by('-id')
    serializer_class = DomainSerialiser
class PaperViewSet(viewsets.ModelViewSet):
    queryset = Paper.objects.all().order_by('-id')
    serializer_class = PagerSerialiser
