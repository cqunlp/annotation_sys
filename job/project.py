# -*- coding: utf-8 -*-
from django.db import models
from user.models import User


class Project(models.Model):
    id = models.AutoField(primary_key=True)
    name=models.CharField(max_length=32)#项目名称
    def __str__(self):
        return self.name


class ProjectRole(models.Model):
    id = models.AutoField(primary_key=True)
    project=models.ForeignKey(Project,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    role=models.IntegerField(default=0)
