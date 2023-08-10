from django.contrib import admin
from .models import Quiz
# Register your models here.

#This allows you to manage the Quiz model through the admin interface
admin.site.register(Quiz)