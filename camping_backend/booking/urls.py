from django.urls import path
from .views import ReservationFormView

urlpatterns = [
    path('make_reservation/', ReservationFormView.as_view(), name='make_reservation'),
]
