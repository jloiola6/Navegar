from django import forms
from .models import Location, Route, Boat

class LocationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LocationForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = "Nome"
    
    class Meta:
        model = Location
        fields = ['name']    
