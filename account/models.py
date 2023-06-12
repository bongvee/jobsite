from django.db import models
# ADDED
from django.contrib.auth.models import User

# ADDED, use makemigrations
class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='userprofile', on_delete=models.CASCADE)
    ident_card = models.FileField(null=True)        # for file upload
