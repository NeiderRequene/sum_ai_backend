from django.db import models

from api.modules.common.basic_abstrac_model.basic_abstrac_model import BasicAbstracModel


class SentMessage(BasicAbstracModel):
    from_email = models.CharField(blank=True, null=True, max_length=255)
    recipient = models.TextField(blank=True, null=True)
    subject = models.TextField(blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    message_id = models.CharField(blank=True, null=True, max_length=255)

    class Meta:
        ordering = ['created_at']
