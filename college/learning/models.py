from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Homework(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)   
    name = models.CharField(max_length=200)
    body = models.TextField()
    is_finished = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    
class Todo(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    is_finished = models.BooleanField(default=False)
    def __str__(self):
        return self.name
