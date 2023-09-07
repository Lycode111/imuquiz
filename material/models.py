from django.db import models

# Create your models here.
class Revision(models.Model):
    name = models.CharField(max_length=120)
    topic = models.CharField(max_length=120) 
    image = models.URLField(default='')
    file = models.FileField(upload_to='materials/')