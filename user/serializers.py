
from rest_framework import serializers
from .models import *


class UserSerialiser(serializers.ModelSerializer):
    subjectname=serializers.CharField(source='subject.name',read_only=True)
    class Meta:
        model = User
        exclude=['password']
        #fields = "__all__"