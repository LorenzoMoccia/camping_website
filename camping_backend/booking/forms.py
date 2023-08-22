from django import forms
from .models import Booking

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['name', 'surname', 'check_in_date', 'check_out_date', 'number_people']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control my-input'
