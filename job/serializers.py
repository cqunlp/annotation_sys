
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

class Job_userSerialiser(serializers.ModelSerializer):
    #user=serializers.HiddenField(default=serializers.CurrentUserDefault())
    subject=serializers.IntegerField(source='paragraph.content.paper.subject.id')
    domain=serializers.IntegerField(source='paragraph.content.paper.domain.id')

    class Meta:
        model = Job_user
        fields = "__all__"
