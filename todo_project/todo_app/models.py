from django.db import models
from django.contrib.auth.models import User


class TodoAppModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True)
    due_datetime = models.DateTimeField(blank=True, auto_now=False)
    completed = models.BooleanField(default=False)
    completed_on_datetime=models.DateTimeField(null=True,blank=True, auto_now=False)
    email_notification_sent = models.BooleanField(default=False)
    created_at_datetime = models.DateTimeField(auto_now_add=True)
    updated_at_datetime = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        ordering = ['completed', 'due_datetime','updated_at_datetime']

    def __str__(self):
        return self.title
