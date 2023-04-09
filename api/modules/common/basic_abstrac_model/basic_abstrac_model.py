from django.db import models


class BasicAbstracModel(models.Model):
    is_deleted = models.BooleanField(null=None, default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    deleted_at = models.DateTimeField(null=True, default=None)

    class Meta:
        abstract = True
