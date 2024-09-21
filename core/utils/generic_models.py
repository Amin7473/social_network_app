import uuid
from django.db import models


class CoreGenericModel(models.Model):
    """
        This class is inherited by all models throught the application
    """
    id = models.UUIDField(default=uuid.uuid1, unique=True, primary_key=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    class Meta:
        """Meta properties"""
        abstract = True
