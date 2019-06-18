# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.


class Subject(models.Model):
    id = models.AutoField('id', primary_key=True)
    name=models.CharField('',max_length=32)


class Paper(models.Model):
    id = models.AutoField('论文id', primary_key=True)
    journal=models.CharField('期刊号',max_length=32)
    journal_tips=models.CharField('期刊信息',max_length=128)
    paper_title=models.CharField('论文标题',max_length=128)
    paper_authors=models.CharField('论文作者',max_length=128)
    keywords=models.CharField('关键词',max_length=128)
    journal_tips=models.CharField('期刊信息',max_length=128)
    subject=models.OneToOneField(Subject, on_delete=models.CASCADE)
    def __str__(self):
        return self.paper_title

class Paper_contents(models.Model):
    id = models.AutoField('id', primary_key=True)
    headline=models.CharField('',max_length=32)
    parent=models.IntegerField('')
    paper=models.OneToOneField(Paper,on_delete=models.DO_NOTHING)


class Paragraph(models.Model):
    id = models.AutoField('id', primary_key=True)
    paragraph_content=models.TextField()
    paragraph_type=models.IntegerField('paragraph_type')
    content=models.OneToOneField(Paper_contents,on_delete=models.DO_NOTHING)
    def __str__(self):
        return self.paragraph_content




