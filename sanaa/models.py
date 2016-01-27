import uuid
from django.db import models

from sanaa.managers import CustomerImageManager

__author__ = 'Nestor Velazquez'


class CustomerImage(models.Model):
    """
    docstring for CustomerImage
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    document = models.FileField()
    thumbnail = models.ImageField()

    objects = CustomerImageManager()
