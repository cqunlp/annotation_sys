# -*- coding: utf-8 -*-
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

# Create your views here.

class AdminWrite(BasePermission):
    def has_permission(self, request, view):
        return (request.method in ['GET','PUT'] and request.user  and request.user.is_authenticated) or request.user.is_staff
    def has_object_permission(self, request, view, obj):
        return (request.method in ['GET','PUT'] and request.user  and request.user.is_authenticated) or request.user.is_staff


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
    filterset_fields =['id','is_staff','username']
    permission_classes = [AdminWrite]
