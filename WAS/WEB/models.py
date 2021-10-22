from django.db import models

# Create your models here.
class FaceImage(models.Model) : 
    faceId = models.AutoField(primary_key=True)
    faceImg = models.ImageField(upload_to='images/')