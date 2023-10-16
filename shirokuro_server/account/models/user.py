from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    birth_date = models.DateField(null=True)
    email = models.EmailField(unique=True, verbose_name="Email address", null=True)
    # language = models.ForeignKey(Language, null=False, on_delete=models.RESTRICT)
    # region = models.ForeignKey(Region, null=False, on_delete=models.RESTRICT)
