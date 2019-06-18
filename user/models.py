# -*- coding: utf-8 -*-
from django.contrib.auth.models import AbstractUser
from django.db import models

# 有个坑，扩展字段后密码会明文，当我们提交的时候需要进行设置，在后面的代码中会提到
class User(AbstractUser):
    test=models.IntegerField()