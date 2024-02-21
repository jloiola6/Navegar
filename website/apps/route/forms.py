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
    
    #Adicionar campos readonly aqui!
    # value_3 = forms.TimeField(widget=TextInput(attrs={'readonly': True}))

    def __init__(self, *args, **kwargs):
        super(RouteForm, self).__init__(*args, **kwargs)
        

    class Meta:
        model = Route
        fields = ['origin', 'destination', 'value', 'value_2', 'value_3', 'value_4', 'departure_time', 'arrival_time', 'after_midnight']