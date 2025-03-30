
from django.db import models

class UploadedImage(models.Model):
    image = models.ImageField(upload_to='images/')
    extracted_text = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
