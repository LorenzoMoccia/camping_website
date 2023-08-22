from django.urls import path
from .views import ReservationFormView, ReservationListView, DeleteReservationView

urlpatterns = [
    path('make_reservation/', ReservationFormView.as_view(), name='make_reservation'),
    path('reservation_list/', ReservationListView.as_view(), name='reservation_list'),
    path('delete_reservation/<int:pk>/', DeleteReservationView.as_view(), name='delete_reservation'),
]
