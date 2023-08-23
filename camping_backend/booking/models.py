from django.db import models

# Create your models here.
class Booking(models.Model):
    name = models.CharField(max_length=150)
    surname = models.CharField(max_length=150)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    number_people = models.IntegerField()

    def __str__(self):
        return f"{self.name} {self.surname}"


