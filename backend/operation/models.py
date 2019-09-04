from django.db import models

# Create your models here.
class Operation(models.Model):
    raw_image = models.CharField(max_length=128)
    raw_image_name = models.CharField(max_length=128, default='image.jpg')
    processed_image_0 = models.CharField(max_length=128, default='')
    processed_image_1 = models.CharField(max_length=128, default='')
    upload_time = models.DateTimeField(auto_now_add=True)
    user_id = models.IntegerField(null=True)

