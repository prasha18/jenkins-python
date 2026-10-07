from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class State(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class District(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='districts')

    def __str__(self):
        return self.name

class Inventor(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    dob = models.DateField()
    aadhaar = models.FileField(upload_to='inventor_aadhaars/', null=True, blank=True)
    mobile = models.CharField(max_length=10, validators=[MinLengthValidator(10)])
    email = models.EmailField()

    def __str__(self):
        return f"{self.name} - Inventor"
    




class Tech_Director(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    dob = models.DateField()
    aadhaar = models.FileField(upload_to='director_aadhaars/', null=True, blank=True)
    mobile = models.CharField(max_length=10, validators=[MinLengthValidator(10)])
    email = models.EmailField()

    def __str__(self):
        return f"{self.name} - Director"