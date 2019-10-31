
from rest_framework import serializers
from .models import *
from paper.models import *





class JobSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = "__all__"

class LabelSerialiser(serializers.ModelSerializer):
    subject=serializers.IntegerField(source='domain.subject.id',read_only=True)

    class Meta:
        model = Label
        fields = "__all__"

class EntitySerialiser(serializers.ModelSerializer):
    user=serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Entity
        fields = "__all__"

class RelationSerialiser(serializers.ModelSerializer):
    user=serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Relation
        fields = "__all__"

class SummarySerialiser(serializers.ModelSerializer):
    user=serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Summary
        fields = "__all__"

class Project_userSerialiser(serializers.ModelSerializer):
    #user=serializers.HiddenField(default=serializers.CurrentUserDefault())
    subject=serializers.IntegerField(source='paragraph.content.paper.subject.id',read_only=True)
    domain=serializers.IntegerField(source='paragraph.content.paper.domain.id',read_only=True)
    paragraph_content=serializers.CharField(source='paragraph.paragraph_content',read_only=True)

    class Meta:
        model = Project_user
        fields = "__all__"


class DispatchedSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Dispatch
        fields = ['paper','project']


class ProjectSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"

class ProjectRoleSerialiser(serializers.ModelSerializer):

    name=serializers.CharField(source='project.name',read_only=True)
    class Meta:
        model = ProjectRole
        fields = "__all__"