from django.contrib import admin
from .models import Question, HighScoreSet, Category

# Register your models here.
admin.site.register(Category)
admin.site.register(HighScoreSet)
admin.site.register(Question)