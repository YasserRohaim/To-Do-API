from django.db import models
from django.contrib.auth.models import User

class Categories(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE)


    def __str__(self):
        return self.name
    
class Tasks(models.Model):
    name=models.CharField(max_length=50)
    description = models.TextField(blank=True)
    deadline=models.DateTimeField(null=True, blank=True)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True, blank=True)
    completed = models.BooleanField(default=False)
    PRIORITY_CHOICES = [
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High'),
    ]
    priority = models.IntegerField(choices=PRIORITY_CHOICES)

    def __str__(self):
        return self.name
