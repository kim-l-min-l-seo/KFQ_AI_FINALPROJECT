# forms.py
from django import forms
from .models import *
  
class FaceForm(forms.ModelForm):
  
    class Meta:
        model = FaceImage
        fields = ['faceId', 'faceImg']