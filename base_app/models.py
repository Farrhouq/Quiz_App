from email.policy import default
from random import choices
from unicodedata import category, name
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    

class Question(models.Model):
    question = models.CharField(max_length=1000, null=False)
    a = models.CharField(max_length=200, null=True )
    b = models.CharField(max_length=200, null=True )
    c = models.CharField(max_length=200, null=True )
    d = models.CharField(max_length=200, null=True )
    e = models.CharField(max_length=200, null=True, blank=True )
    possible = (
        ('a', 'a'),
        ('b', 'b'),
        ('c', 'c'),
        ('d', 'd')
    )
    answer = models.CharField(max_length=1, choices=possible, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    points = models.IntegerField()

class HighScoreSet(models.Model):
    category = models.OneToOneField(Category, on_delete=models.CASCADE)
    data = list()

class UserResults(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    

