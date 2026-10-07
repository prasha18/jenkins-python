import random
import string
from django.db import models

class Sector(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

def generate_custom_id():
    def generate_unique_id():
        while True:
            prefix = ''.join(random.choices(string.ascii_uppercase, k=2))
            suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
            new_id = f"{prefix}{suffix}"
            if not Technology.objects.filter(unique_id=new_id).exists():
                return new_id
    return generate_unique_id()

class Technology(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=250)
    pdf = models.FileField(upload_to='pdfs/')
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    unique_id = models.CharField(max_length=6, unique=True, null=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.unique_id:
            self.unique_id = generate_custom_id()
        super().save(*args, **kwargs)

class ContactSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email} - {self.submitted_at}"