from django.db import models
from django.contrib.auth.models import User


class Image(models.Model):
    owner = models.ForeignKey(User)
    studyid = models.CharField(max_length=10)
    date = models.DateField()
    image = models.FileField()

User.profile = property(lambda u: Image.objects.get_or_create(owner=u)[0])
