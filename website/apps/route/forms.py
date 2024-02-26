from django import forms
from django.forms import inlineformset_factory
from django.forms.widgets import TextInput
from django.forms.models import BaseInlineFormSet

from .models import Location, RouteWeekday, Route

class LocationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LocationForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = "Nome"
    
    class Meta:
        model = Location
        fields = ['name']    

class RouteWeekdayForm(forms.ModelForm):
    class Meta:
        model = RouteWeekday
        fields = ['weekday', 'boat']

class CustomRouteWeekdayFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for form in self.forms:
            form.fields.pop('id')
            form.fields.pop('route')

RouteWeekdayFormSet = inlineformset_factory(Route, RouteWeekday, form=RouteWeekdayForm, extra=1, formset=CustomRouteWeekdayFormSet)

class RouteForm(forms.ModelForm):
    departure_time = forms.TimeField(widget=TextInput(attrs={'type': 'time'}))
    arrival_time = forms.TimeField(widget=TextInput(attrs={'type': 'time'}))

    class Meta:
        model = Route
        fields = ['origin', 'destination', 'value', 'departure_time', 'arrival_time', 'after_midnight']