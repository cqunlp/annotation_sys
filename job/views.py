# -*- coding: utf-8 -*-
from django.shortcuts import render
from .serializers import *
from rest_framework import viewsets,filters
from rest_framework.permissions import *
from rest_framework.decorators import action
from django.shortcuts import HttpResponse
from django.db.models import Count
from django.db import connection
import MySQLdb.cursors
import json
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework import status
# Create your views here.


class AdminWrite(BasePermission):
    def has_permission(self, request, view):
        return (request.method in ['GET','PUT'] and request.user  and request.user.is_authenticated) or request.user.is_staff
    def has_object_permission(self, request, view, obj):
        return (request.method in ['GET','PUT'] and request.user  and request.user.is_authenticated) or request.user.is_staff

class Projectpermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        pr = ProjectRole.objects.filter(user=request.user, role=1).count()
        if pr > 0:
            return True
        return (request.method in SAFE_METHODS and request.user  and request.user.is_authenticated) or request.user.is_staff
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        if request.method in ['DELETE','PUT','POST']:
            pr = ProjectRole.objects.filter(user=request.user,project=obj.project, role=1).count()
            if pr>0:
                return True
        return (request.method in SAFE_METHODS and request.user  and request.user.is_authenticated) or request.user.is_staff

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()#.order_by('-id')
    serializer_class = ProjectSerialiser
    filterset_fields = ['id', 'name']
    search_fields = ['name']


class ProjectRoleViewSet(viewsets.ModelViewSet):
    queryset = ProjectRole.objects.all()#.order_by('-id')
    serializer_class = ProjectRoleSerialiser
    #filterset_fields = ['project', 'user','role']
    #search_fields = ['name']
    permission_classes = [Projectpermission]

    def create(self, request):
        new = ProjectRole.objects.filter(user=request.data['user'], project=request.data['project']).count()
        if new == 0:
            pr = ProjectRole.objects.filter(user=request.user, project=request.data['project'], role=1).count()
            if pr > 0 or request.user.is_staff:
                return super().create(request)

        return HttpResponse("403")



class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all().order_by('-id')
    serializer_class = JobSerialiser
    filterset_fields = ['id', 'name']
    search_fields = ['name','job_table']


class LabelViewSet(viewsets.ModelViewSet):
    queryset = Label.objects.all().order_by('-id')
    serializer_class = LabelSerialiser
    filterset_fields = ['id', 'name','domain','job']
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


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
def DownloadJson(request):
    c=connection.cursor()
    c.execute("select p.paragraph_content as sentense , e.start_offset ,e.end_offset , e.label_id ,e.`name`  from paper_paragraph p ,job_entity e WHERE e.paragraph_id=p.id ")
    file = open('json', 'w',encoding='utf-8')
    file.write(json.dumps(dictfetchall(c),ensure_ascii=False))
    file.close()
    file = open('json', 'rb')
    response = HttpResponse(file)
    file.close()
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="json.txt"'
    return response