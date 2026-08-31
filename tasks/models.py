from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Task(models.Model):
    STATE_CHOICES = [
        ('TODO' , 'To Do'),
        ('IN_PROGRESS' , 'In Progress'),
        ('DONE' , 'Done'),
    ]
    task_name = models.CharField(max_length=200)
    task_description = models.TextField()
    state = models.CharField(max_length=20, choices=STATE_CHOICES,default='TODO')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    content = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
