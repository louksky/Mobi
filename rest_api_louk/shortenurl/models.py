from django.db import models
from django.conf import settings
# Create your models here.
MAX_URL_LEN_CAN_HANDLE = 4000
class Shortener(models.Model):
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True)
    url = models.TextField(blank=True, default='', max_length=MAX_URL_LEN_CAN_HANDLE)
    shortener = models.TextField(blank=True, default='', max_length=MAX_URL_LEN_CAN_HANDLE, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return '/{}'.format(self.shortener)
    
    class Meta:
        ordering = ['created_at']