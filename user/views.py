# -*- coding: utf-8 -*-
import json
from django.shortcuts import render
from .serializers import *
from rest_framework import viewsets,filters
from rest_framework.permissions import *
from rest_framework.decorators import action
from django.shortcuts import HttpResponse
from django.db.models import Count
from django.shortcuts import render
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render
from django.shortcuts import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from job.models import ProjectRole
# Create your views here.

class AdminWrite(BasePermission):
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS and request.user  and request.user.is_authenticated) or request.user.is_staff
    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS and request.user  and request.user.is_authenticated) or request.user.is_staff


def login_view(request):
    if 'next' in request.GET:
        request.session['next']=request.GET['next']
    return render(request,'user/login.html',)



def login_post(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        request.session['uid']=user.id
        return HttpResponseRedirect(request.session['next'] if 'next' in request.session else '/')
    else:
        # Return an 'invalid login' error message.
        return HttpResponse("Wrong password")

@login_required
def logout_view(request):
    logout(request)
    request.session.clear()
    return HttpResponseRedirect('/user/login')

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerialiser
    filterset_fields =['id','is_staff','username','role']
    permission_classes = [AdminWrite]

    @action(detail=True, methods=['get'])
    def set_teacher(self, request, pk=None):
        u = self.get_object()
        subject = request.GET['subject_id']
        u.subject_id=subject
        u.role=1
        sj=Subject.objects.get(id=subject)
        u.save()
        return HttpResponse(sj.name)
    @action(detail=True, methods=['get'])
    def del_teacher(self, request, pk=None):
        u = self.get_object()
        u.subject_id=None
        u.role=0
        u.save()
        return HttpResponse('success')


def reg(request):
    body=json.loads(request.body.decode('utf-8'))
    username = body['username']
    password = body['password']
    User(username=username,password=make_password(password),is_active=1).save()
    return HttpResponse("success")

