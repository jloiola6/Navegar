from django import forms

from apps.ticket.models import Ticket

class TicketForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)
        self.fields['document'].widget.attrs['accept'] = "image/*"

    class Meta:
        model = Ticket
        fields = ['document']
