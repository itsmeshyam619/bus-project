from django.contrib import admin
from .models import BusSchedule, Booking
# include Booking too if not already

@admin.register(BusSchedule)
class BusScheduleAdmin(admin.ModelAdmin):
    list_display = ('bus_no', 'departure_place', 'destination_place', 'start_time', 'available_seats')
    list_filter = ('departure_place', 'destination_place', 'start_time')  # 🧭 Add filtering
    search_fields = ('bus_no', 'departure_place', 'destination_place')
    ordering = ('start_time',)  # 🕓 Optional: order by time

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'bus', 'booking_time', 'seats_booked')
    search_fields = ('user__username', 'bus__bus_no')
    list_filter = ('booking_time',)
    ordering = ('-booking_time',)
# busapp/admin.py
'''from django.contrib import admin
from .models import BusSchedule, Booking, LocationUpdate, BookingHistory'''

'''@admin.register(BusSchedule)
class BusScheduleAdmin(admin.ModelAdmin):
    list_display = ('bus_no', 'departure_place', 'destination_place', 'start_time', 'available_seats')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'bus', 'seats_booked', 'booking_time')'''

'''@admin.register(LocationUpdate)
class LocationUpdateAdmin(admin.ModelAdmin):
   list_display = ('bus', 'latitude', 'longitude', 'timestamp')

@admin.register(BookingHistory)
class BookingHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'bus', 'seats_booked', 'booking_time')
'''