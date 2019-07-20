# -*- coding: utf-8 -*-
from django.shortcuts import render
from .serializers import *
from rest_framework import viewsets,filters
from rest_framework.permissions import *

# Create your views here.


class AdminWrite(BasePermission):
    def has_permission(self, request, view):
        return (request.method in ['GET','PUT'] and request.user  and request.user.is_authenticated) or request.user.is_staff
    def has_object_permission(self, request, view, obj):
        return (request.method in ['GET','PUT'] and request.user  and request.user.is_authenticated) or request.user.is_staff


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all().order_by('-id')
    serializer_class = JobSerialiser
    filterset_fields = ['id', 'name']
    search_fields = ['name','job_table']


class LabelViewSet(viewsets.ModelViewSet):
    queryset = Label.objects.all().order_by('-id')
    serializer_class = LabelSerialiser
    filterset_fields = ['id', 'name','subject','domain','job']
    search_fields = ['name']


class EntityViewSet(viewsets.ModelViewSet):
    queryset = Entity.objects.all().order_by('start_offset')
    serializer_class = EntitySerialiser
    filterset_fields = ['id', 'paragraph','label','user']
    #search_fields = ['paper_title','keywords',]


class RelationViewSet(viewsets.ModelViewSet):
    queryset = Relation.objects.all().order_by('-id')
    serializer_class = RelationSerialiser
    filterset_fields = ['id', 'label','user']
    #search_fields = ['headline']

class SummaryViewSet(viewsets.ModelViewSet):
    queryset = Summary.objects.all().order_by('-id')
    serializer_class = SummarySerialiser
    filterset_fields = ['id', 'paragraph','user']
    #search_fields = ['paragraph_content']


class Job_userViewSet(viewsets.ModelViewSet):
    queryset = Job_user.objects.all().order_by('-id')
    serializer_class = Job_userSerialiser
    filterset_fields = ['id', 'user','paragraph','job','status']
    #search_fields = ['paragraph_content']
    permission_classes = [AdminWrite]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Job_user.objects.all().order_by('-id')

        return Job_user.objects.filter(user=user)

