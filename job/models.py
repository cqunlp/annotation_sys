# -*- coding: utf-8 -*-
from django.db import models
from paper.models import Subject,Paragraph,Paper
from user.models import User
# Create your models here.



class Job(models.Model):
    id = models.AutoField(primary_key=True)
    name=models.CharField(max_length=32)
    job_table=models.CharField(max_length=32)

class Label(models.Model):
    id = models.AutoField(primary_key=True)
    name=models.CharField(max_length=32)
    shortcut=models.CharField(max_length=32)
    background_color=models.CharField(max_length=32)
    text_color=models.CharField(max_length=32)
    subject=models.OneToOneField(Subject,on_delete=models.CASCADE)
    job = models.OneToOneField(Job,on_delete=models.CASCADE)

class Entity(models.Model):
    id = models.AutoField(primary_key=True)
    start_offset=models.IntegerField()
    end_offset=models.IntegerField()
    paragraph=models.OneToOneField(Paragraph,on_delete=models.CASCADE)
    label=models.OneToOneField(Label,on_delete=models.CASCADE)
    user=models.OneToOneField(User,on_delete=models.CASCADE)

class Relation(models.Model):
    id = models.AutoField(primary_key=True)
    entity1=models.OneToOneField(Entity,on_delete=models.CASCADE,related_name='Relation_entity1')
    entity2=models.OneToOneField(Entity,on_delete=models.CASCADE,related_name='Relation_entity2')
    label=models.OneToOneField(Label,on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Summary(models.Model):
    id = models.AutoField(primary_key=True)
    paragraph=models.ForeignKey(Paragraph,on_delete=models.CASCADE)
    label=models.OneToOneField(Label,on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Job_user(models.Model):
    id = models.AutoField(primary_key=True)
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    paper=models.OneToOneField(Paper,on_delete=models.CASCADE)
    job=models.OneToOneField(Job,on_delete=models.CASCADE)
    status=models.BooleanField()

