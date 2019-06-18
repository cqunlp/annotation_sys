from django.db import models

# Create your models here.


class Subject(models.Model):
    id = models.AutoField('id', primary_key=True)
    name=models.CharField('',max_length=32)


class Paper(models.Model):
    id = models.AutoField('论文id', primary_key=True)
    journal_id=models.CharField('期刊号',max_length=32)
    journal_tips=models.CharField('期刊信息',max_length=128)
    paper_title=models.CharField('论文标题',max_length=128)
    paper_authors=models.CharField('论文作者',max_length=128)
    keywords=models.CharField('关键词',max_length=128)
    journal_tips=models.CharField('期刊信息',max_length=128)
    subject_id=models.ForeignKey('学科',Subject,on_delete=models.CASCADE)
    def __str__(self):
        return self.paper_title

class Paper_contents(models.Model):
    id = models.AutoField('id', primary_key=True)
    headline=models.CharField('',max_length=32)
    parent_id=models.IntegerField('')
    paper_id=models.ForeignKey('',Paper,on_delete=models.CASCADE)


class Paragraph(models.Model):
    id = models.AutoField('id', primary_key=True)
    paragraph_content=models.TextField()
    paragraph_type=models.IntegerField('paragraph_type')
    content_id=models.ForeignKey('',Paper_contents,on_delete=models.CASCADE)
    def __str__(self):
        return self.paragraph_content




