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
    departure_time.label = 'Horário de partida'

    arrival_time = forms.TimeField(widget=TextInput(attrs={'type': 'time'}))
    arrival_time.label = 'Horário de chegada'

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(RouteForm, self).__init__(*args, **kwargs)

        if user and user.discount:
            # Fazer verificação de desconto
            pass

        self.fields['discounted_value'].widget.attrs['readonly'] = True
        self.fields['discounted_cost'].widget.attrs['readonly'] = True

        self.fields['after_midnight'].widget.attrs['class'] = 'next-day-check'

    class Meta:
        model = Route
        fields = ['origin', 'destination', 'value', 'discounted_value', 'cost_value', 'discounted_cost', 'departure_time', 'arrival_time', 'after_midnight']