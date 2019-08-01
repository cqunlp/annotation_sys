# -*- coding: utf-8 -*-
from django.shortcuts import render
from .serializers import *
from rest_framework import viewsets,filters
from rest_framework.permissions import *
from rest_framework.decorators import action
from django.shortcuts import HttpResponse
from django.db.models import Count

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
    filterset_fields = ['id', 'label','user','entity1','entity2']
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

    @action(detail=True, methods=['get'])
    def set_status_true(self, request, pk=None):
        ujob = self.get_object()
        ujob.status=True
        ujob.save()
        return HttpResponse('success')

    @action(detail=True, methods=['get'])
    def set_status_false(self, request, pk=None):
        ujob = self.get_object()
        ujob.status=False
        ujob.save()
        return HttpResponse('success')

    @action(detail=False, methods=['get'])
    def Dispatchjob(self,request, pk=None):
        userid=request.GET['user_id']
        jobid=request.GET['job_id']
        paperid = request.GET['paper_id']
        paragraphs = Paragraph.objects.filter(content__paper__id=paperid)
        for i in paragraphs:
            u=Job_user(user_id=userid,job_id=jobid,paragraph_id=i.id,status=0)
            u.save()
        return HttpResponse('success')



class DispatchedViewSet(viewsets.ModelViewSet):
    queryset = Dispatch.objects.all()
    serializer_class = DispatchedSerialiser
    filterset_fields =['paper','job']
