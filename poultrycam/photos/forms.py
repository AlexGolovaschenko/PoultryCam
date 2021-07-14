from django import forms

from .models import Photo

class PhotoMarkersForm(forms.Form):
    id = forms.IntegerField()
