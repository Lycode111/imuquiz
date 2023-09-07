from django.contrib import admin
from .models import Result, Analysis, UserResult

# Register your models here.

# This allows you to manage the Result model through the admin interface
admin.site.register(Result)
admin.site.register(Analysis)
admin.site.register(UserResult)


