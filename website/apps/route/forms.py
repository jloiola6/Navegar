from django import forms
from .models import Location, Route, Boat

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name']    
