from django.db import models

from account.models import User


class CommonFields(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.RESTRICT, null=False)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.RESTRICT, null=False)
    metadata_provider = models.URLField(null=True)

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=[
                '-updated_at',
            ]),
        ]
