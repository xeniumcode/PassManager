from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class UserPassword(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=500)
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=False, blank=False)