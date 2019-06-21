
from rest_framework import serializers
from .models import *





class JobSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = "__all__"

class LabelSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = "__all__"

class EntitySerialiser(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = "__all__"

class RelationSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Relation
        fields = "__all__"

class SummarySerialiser(serializers.ModelSerializer):
    class Meta:
        model = Summary
        fields = "__all__"

class Job_userSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Job_user
        fields = "__all__"