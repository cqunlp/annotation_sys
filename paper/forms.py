from django.forms import ModelForm
from .models import *




class SubjectForm(ModelForm):
    class Meta:
        model=Subject
        exclude = []