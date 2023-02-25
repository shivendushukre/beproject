from django.db import models
from django.contrib.auth.models import User

class Research_Papers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    paper = models.FileField(upload_to='papers/')
    
    def __str__(self):
        return f"{self.paper}"