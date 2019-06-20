# api/utils/serializsers/pager.py

from rest_framework import serializers
from .models import *



class SubjectSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"

class DomainSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = "__all__"

class PagerSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Paper
        fields = "__all__"