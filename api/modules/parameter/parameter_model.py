from django.db import models
from api.modules.common.basic_abstrac_model.basic_abstrac_model import BasicAbstracModel


class Parameter(BasicAbstracModel):
    code = models.CharField(
        blank=True, null=True, max_length=255, default='', unique=True)
    description = models.TextField(blank=True, default='')

    class Meta:
        managed = True
        db_table = 'api_parameter'
        ordering = ['created_at']
