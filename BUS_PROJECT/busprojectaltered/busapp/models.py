from django.db import models, transaction
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class LocationUpdate(models.Model):
    bus = models.ForeignKey('BusSchedule', on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bus.bus_number} at {self.timestamp}"
    
class BusSchedule(models.Model):
    bus_no = models.CharField(max_length=10)
    route_id = models.CharField(max_length=10, default=1)
    departure_place = models.CharField(max_length=60, default="Arapalayam")
    destination_place = models.CharField(max_length=60, default="Arapalayam")
    start_time = models.TimeField()
    available_seats = models.IntegerField(default=40)
    # Add these fields to BusSchedule model
    current_latitude = models.FloatField(null=True, blank=True)
    current_longitude = models.FloatField(null=True, blank=True)


    def __str__(self):
        return f"{self.bus_no} ({self.departure_place} → {self.destination_place})"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bus = models.ForeignKey(BusSchedule, on_delete=models.CASCADE)
    booking_time = models.DateTimeField(auto_now_add=True)
    seats_booked = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.bus.bus_no} ({self.seats_booked} seat(s))"

    def save(self, *args, **kwargs):
        with transaction.atomic():
            bus = BusSchedule.objects.select_for_update().get(id=self.bus.id)
            if self.seats_booked > bus.available_seats:
                raise ValidationError("Not enough seats available!")
            bus.available_seats -= self.seats_booked
            bus.save()
            super().save(*args, **kwargs)



