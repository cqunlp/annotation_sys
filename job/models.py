# -*- coding: utf-8 -*-
from django.db import models
from paper.models import Paragraph,Paper,Domain
# Create your models here.
from user.models import User
from paper.models import Subject



class Job(models.Model):
    id = models.AutoField(primary_key=True)
    name=models.CharField(max_length=32)#任务名称
    job_table=models.CharField(max_length=32)#任务对应数据表


    def __str__(self):
        return self.name


class Project(models.Model):
    id = models.AutoField(primary_key=True)
    name=models.CharField(max_length=32)#项目名称
    domain=models.ForeignKey(Domain,on_delete=models.CASCADE)
    job=models.ForeignKey(Job,on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ProjectRole(models.Model):
    id = models.AutoField(primary_key=True)
    project=models.ForeignKey(Project,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)


class Label(models.Model):
    id = models.AutoField(primary_key=True)
    name=models.CharField(max_length=32)#标签名称
    shortcut=models.CharField(max_length=32)#标签快捷键
    background_color=models.CharField(max_length=32)#背景颜色
    text_color=models.CharField(max_length=32)#文字颜色
    #subject=models.ForeignKey(Subject,on_delete=models.CASCADE)#学科
    domain=models.ForeignKey(Domain,on_delete=models.CASCADE)#领域
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    def __str__(self):
        return self.name
class Entity(models.Model):
    id = models.AutoField(primary_key=True)
    name=models.CharField(max_length=64)#实体名称
    start_offset=models.IntegerField()#开始偏移
    end_offset=models.IntegerField()#结束偏移
    paragraph=models.ForeignKey(Paragraph,on_delete=models.CASCADE)#文章的段落
    label=models.ForeignKey(Label,on_delete=models.CASCADE)#标签
    user=models.ForeignKey(User,on_delete=models.CASCADE)#用户
    def __str__(self):
        return self.name

class Relation(models.Model):
    id = models.AutoField(primary_key=True)
    entity1=models.ForeignKey(Entity,on_delete=models.CASCADE,related_name='Relation_entity1')#实体1
    entity2=models.ForeignKey(Entity,on_delete=models.CASCADE,related_name='Relation_entity2')#实体2
    label=models.ForeignKey(Label,on_delete=models.CASCADE)#标签
    user = models.ForeignKey(User, on_delete=models.CASCADE)#用户

class Summary(models.Model):
    id = models.AutoField(primary_key=True)
    paragraph=models.ForeignKey(Paragraph,on_delete=models.CASCADE)#段落
    label=models.ForeignKey(Label,on_delete=models.CASCADE)#标签
    user = models.ForeignKey(User, on_delete=models.CASCADE)#用户

class Project_user(models.Model):
    id = models.AutoField(primary_key=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE)#用户
    paragraph = models.ForeignKey(Paragraph, on_delete=models.CASCADE)  # 文章的段落
    # paper=models.ForeignKey(Paper,on_delete=models.CASCADE)#文章
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    status=models.BooleanField()#状态

class Dispatch(models.Model):
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project,on_delete=models.DO_NOTHING)
    paper=models.ForeignKey(Paper,on_delete=models.DO_NOTHING)
    class Meta:
        db_table='dispatched'