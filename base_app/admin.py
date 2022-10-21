from django.contrib import admin
from .models import Question, Category

# Register your models here.
admin.site.register(Category)
admin.site.register(Question)