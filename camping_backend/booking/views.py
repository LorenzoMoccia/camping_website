from django.views.generic.edit import FormView
from .forms import ReservationForm
from .models import Booking
from django.urls import reverse_lazy

class ReservationFormView(FormView):
    form_class = ReservationForm
    template_name = 'booking/booking_form.html'
    success_url = reverse_lazy('make_reservation')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
