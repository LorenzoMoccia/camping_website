from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('booking.urls')),  # Aggiungi questa riga per l'applicazione "booking"
]

urlpatterns += [path("__debug__/", include("debug_toolbar.urls")),]