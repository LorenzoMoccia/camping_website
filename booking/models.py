from django.db import models
from django.utils.translation import gettext_lazy as _

class Booking(models.Model):
    check_in_date = models.DateField(blank=False, verbose_name=_("Data Check-in"))
    check_out_date = models.DateField(blank=False, verbose_name=_("Data Check-out"))
    number_people = models.PositiveIntegerField()
    client = models.ForeignKey("booking.Client", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.pk} {self.check_in_date} -> {self.check_out_date}"


class Client(models.Model):
    name = models.CharField(max_length=150, verbose_name=_("Nome"))
    surname = models.CharField(max_length=150, verbose_name=_("Cognome"))
    email = models.EmailField()
    phone = models.CharField(max_length=16, verbose_name=_("Numero di telefono"))
    def __str__(self):
        return f"{self.name} {self.surname}"
