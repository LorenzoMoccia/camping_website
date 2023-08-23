from django.views.generic.edit import FormView
from .forms import ReservationForm
from .models import Booking
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.base import View

def index(request):
    return render(request, 'index.html')

class ReservationFormView(FormView):
    form_class = ReservationForm
    template_name = 'booking/booking_form.html'
    success_url = reverse_lazy('make_reservation')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
class ReservationListView(View):
    def get(self, request):
        reservations = Booking.objects.all()
        return render(request, 'booking/booking_list.html', {'reservations': reservations})

    def post(self, request):
        reservation_id = request.POST.get('reservation_id')
        if reservation_id:
            reservation = Booking.objects.get(pk=reservation_id)
            reservation.delete()
        return redirect('reservation_list')

class DeleteReservationView(View):
    def get(self, request, pk):
        reservation = Booking.objects.get(pk=pk)
        reservation.delete()
        return redirect('reservation_list')
