from django.db import models

from api.modules.user.models.user_model import User


class Binnacle(models.Model):
    table_name = models.CharField(blank=True, null=True, max_length=255)
    transaction = models.CharField(blank=True, null=True, max_length=255)
    query = models.TextField(blank=True, null=True, default='')
    ip = models.CharField(blank=True, null=True, max_length=255)
    user = models.ForeignKey(
        User, related_name='binnacle', on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
