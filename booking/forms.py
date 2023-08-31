from django import forms
from .models import Booking

class ReservationForm(forms.ModelForm):
    # todo
    # aggiungere che si colleghi a uno user
    # user dovra prima registrarsi (anche sulla stessa pag in ajax) e così associamo prenotazione a user

    class Meta:
        model = Booking
        fields = ['check_in_date', 'check_out_date', 'number_people']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control my-input'
