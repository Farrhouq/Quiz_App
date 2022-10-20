from dataclasses import fields
import imp
from django.forms import ModelForm
from . import models
from django.contrib.auth.models import User

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class QuestionForm(ModelForm):
    class Meta:
        model = models.Question
        exclude = ['category']

