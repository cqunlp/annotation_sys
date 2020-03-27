# -*- coding: utf-8 -*-
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from .models import *
from .forms import *
import time
import json
from django.core import serializers
import os
from uuid import uuid4
from werkzeug.utils import secure_filename

from django.db import connections

from .serializers import *
from rest_framework import viewsets,filters
from rest_framework.permissions import *
from rest_framework.authtoken.models import Token
# Create your views here.

class AdminWrite(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_staff:
            return True
        if request.user.subject is not None:
            return True
        return (request.method in SAFE_METHODS and request.user  and request.user.is_authenticated) or request.user.is_staff or request.user.subject is not None
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        if isinstance(obj,Subject):
            return (request.method in SAFE_METHODS and request.user  and request.user.is_authenticated)
            #obj=obj.project
        if isinstance(obj,Paragraph):
            obj=obj.content
        if isinstance(obj,Paper_contents):
            obj=obj.paper
        if isinstance(obj,Paper):
            obj=obj.domain
        if isinstance(obj,Domain):
            obj=obj.subject


        if request.method in ['DELETE','PUT','POST']:
            if request.user.subject.id==obj.id:
                return True
        return (request.method in SAFE_METHODS and request.user  and request.user.is_authenticated) or request.user.is_staff


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all().order_by('-id')
    serializer_class = SubjectSerialiser
    filterset_fields = ['id', 'name']
    search_fields = ['name']
    permission_classes = [AdminWrite]
    def create(self, request):
        #
        sj=super().create(request)
        #u=User.objects.get(id=sj.data['id'])
        return sj

class DomainViewSet(viewsets.ModelViewSet):
    queryset = Domain.objects.all().order_by('-id')
    serializer_class = DomainSerialiser
    filterset_fields = ['id', 'name']
    search_fields = ['name']
    permission_classes = [AdminWrite]
    def get_queryset(self):
        queryset = Domain.objects.filter(subject__id=self.request.user.subject_id).order_by('-id')
        return queryset

class PaperViewSet(viewsets.ModelViewSet):
    queryset = Paper.objects.all().order_by('-id')
    serializer_class = PaperSerialiser
    filterset_fields = ['id', 'paper_title','keywords','domain']
    search_fields = ['paper_title',]
    permission_classes = [AdminWrite]

class PaperundispatchedViewSet(viewsets.ModelViewSet):

    queryset = Paper.objects.all()
    serializer_class = PaperSerialiser
    filterset_fields = ['id','keywords','domain']
    search_fields = ['paper_title','keywords',]
    permission_classes = [AdminWrite]
    def get_queryset(self):
        pid=self.request.GET['project_id']
        did=self.request.GET['domain']
        pps = Paperundispatched2.objects.filter(project_id=pid).order_by('-id')
        ids = []
        for i in pps:
            ids.append(i.paper_id)
        queryset = Paper.objects.filter(domain_id=did).exclude(id__in=ids)
        return queryset

class Paper_contentsViewSet(viewsets.ModelViewSet):
    queryset = Paper_contents.objects.all().order_by('-id')
    serializer_class = Paper_contentsSerialiser
    filterset_fields = ['id', 'parent','paper']
    search_fields = ['headline']
    permission_classes = [AdminWrite]


class ParagraphViewSet(viewsets.ModelViewSet):
    queryset = Paragraph.objects.all().order_by('-id')
    serializer_class = ParagraphSerialiser
    filterset_fields = ['id', 'paragraph_type','content']
    search_fields = ['paragraph_content']
    permission_classes = [AdminWrite]


ALLOWED_EXTENSIONS = set(['txt', 'json'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def reg_paper(request):

    token=request.GET['token']
    domain=request.GET['domain']


    if Token.objects.filter(key=token).exists():
        f = request.FILES['myfile']
        if not (f and allowed_file(f.name)):
            return HttpResponse("请检查上传的类型，仅限于txt,json")
        basepath = os.path.dirname(__file__)  # 当前文件所在路径
        filename = '{}.{}'.format(uuid4().hex, 'txt')
        upload_path = os.path.join(basepath, 'paper_upload', secure_filename(filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径

        n=f.read().decode('gbk')
        bodys = json.loads(n)

        for body in bodys:
            p = Paper(journal=body['journal'], journal_tips=body['journal_tips'], paper_authors=body['paper_authors'],
                      paper_title=body['paper_title'], keywords=body['keywords'], filename=body['filename'],
                      domain_id=domain)
            p.save()
            for i in body['contents']:
                c = Paper_contents(headline=i['headline'], parent=i['parent'], paper_id=p.id)
                c.save()
                for j in i['paragraphs']:
                    Paragraph(content_id=c.id, paragraph_content=j['paragraph_content'],
                              paragraph_type=j['paragraph_type']).save()

        return HttpResponse("success")
    return HttpResponse("403")



