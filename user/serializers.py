
from rest_framework import serializers
from .models import *


class UserSerialiser(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude=['password']
        #fields = "__all__"