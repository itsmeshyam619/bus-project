from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import BusSchedule, Booking
from .forms import BusSearchForm
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import LocationUpdate
import requests

from redmail import gmail
from smtplib import SMTPAuthenticationError, SMTPRecipientsRefused, SMTPSenderRefused, SMTPException
@login_required
@csrf_exempt
def book_bus_ajax(request):
    if request.method == 'POST':
        bus_id = request.POST.get('bus_id')
        seats = int(request.POST.get('seats', 1))
        try:
            bus = BusSchedule.objects.get(id=bus_id)
            if bus.available_seats >= seats:
                booking = Booking.objects.create(user=request.user, bus=bus, seats_booked=seats)
                return JsonResponse({
                    'success': True,
                    'message': 'Booking successful!',
                    'new_seat_count': bus.available_seats
                })
            else:
                return JsonResponse({'success': False, 'message': 'Not enough seats available!'}, status=400)
        except BusSchedule.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Bus not found.'}, status=404)

    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)


@login_required
def book_bus(request):
    if request.method == 'POST':
        bus_id = request.POST.get('bus_id')
        seats = int(request.POST.get('seats', 1))
        try:
            bus = BusSchedule.objects.get(id=bus_id)
            if bus.available_seats >= seats:
                Booking.objects.create(user=request.user, bus=bus, seats_booked=seats)
                return render(request, 'confirmation.html', {'bus': bus, 'seats': seats})
            else:
                return render(request, 'error.html', {'message': 'Not enough seats available!'})
        except BusSchedule.DoesNotExist:
            return render(request, 'error.html', {'message': 'Bus not found.'})
    return redirect('schedule')


def start(request):
    return render(request, "index.html")


def take_schedule(request):
    return render(request, "schedule.html")


def search_bus(request):
    buses = []
    if request.method == 'POST':
        from_location = request.POST.get('from')
        to_location = request.POST.get('to')
        time_input = request.POST.get('time')

        print("FROM:", from_location)
        print("TO:", to_location)
        print("TIME:", time_input)

        if from_location and to_location and time_input:
            try:
                time_obj = datetime.strptime(time_input, '%H:%M').time()
                buses = BusSchedule.objects.filter(
                    departure_place__iexact=from_location.strip(),
                    destination_place__iexact=to_location.strip(),
                    start_time__gte=time_obj
                ).order_by('start_time')

                print("BUSES FOUND:", buses)
            except ValueError:
                print("Invalid time format")
    return render(request, 'schedule.html', {'buses': buses})



def bus_schedule_search(request):
    available_buses = None
    form = BusSearchForm()

    if request.method == "POST":
        form = BusSearchForm(request.POST)
        if form.is_valid():
            selected_time = form.cleaned_data['time']
            available_buses = BusSchedule.objects.filter(start_time__gte=selected_time)

    return render(request, 'busapp/bus_schedule_search.html', {
        'form': form,
        'available_buses': available_buses
    })



@csrf_exempt
def update_bus_location(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            bus = BusSchedule.objects.get(bus_no=data['bus_no'])
            bus.current_latitude = data['latitude']
            bus.current_longitude = data['longitude']
            bus.save()
            LocationUpdate.objects.create(bus=bus, latitude=data['latitude'], longitude=data['longitude'])
            return JsonResponse({'status': 'success'})
        except BusSchedule.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Bus not found'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

def get_bus_location(request, bus_no):
    try:
        bus = BusSchedule.objects.get(bus_no=bus_no)
        return JsonResponse({
            'bus_no': bus.bus_no,
            'latitude': bus.current_latitude,
            'longitude': bus.current_longitude
        })
    except BusSchedule.DoesNotExist:
        return JsonResponse({'error': 'Bus not found'}, status=404)
# views.py
def track_bus(request, bus_id):
    try:
        bus = BusSchedule.objects.get(id=bus_id)
        print(bus)
        return render(request, 'track_bus.html', {'bus': bus})
    except BusSchedule.DoesNotExist:
        return render(request, 'error.html', {'message': 'Bus not found.'})


def booking_history(request):
    # You can customize this later
    return render(request, 'booking_history.html')


from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication



@csrf_exempt
def book_bus_ajax(request):
    if request.method == 'POST':
        bus_id = request.POST.get('bus_id')
        seats = int(request.POST.get('seats'))
        email = request.POST.get('mail')

        # Get the bus object
        bus = get_object_or_404(BusSchedule, id=bus_id)

        if bus.available_seats >= seats:
            # Reduce available seats
            bus.available_seats -= seats
            bus.save()
            send_mail(email)


            return JsonResponse({'success': True, 'bus_no': bus.bus_no})
        else:
            return JsonResponse({'success': False, 'message': 'Not enough seats available.'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

def send_mail(email):
    gmail.username = "shukk.56@gmail.com"  # Replace with your actual Gmail username
    gmail.password = "gsar enfw yvvp mvty"  # Replace with your Gmail app password
    print(email)
    print(type(email))
    try:
        gmail.send(
            subject="Booking Confirmation",
            receivers=[email],
            text="After the payment you have receive the E-ticket",
            html=f"<p>https://www.phonepe.com/</p>"
        )
    except SMTPRecipientsRefused:
        raise ValueError("The recipient email address is invalid.")
    except SMTPSenderRefused:
        raise ValueError("The sender's email credentials are incorrect.")
    except SMTPAuthenticationError:
        raise ValueError("Authentication failed. Check your Gmail credentials.")
    except SMTPException as e:
        raise ValueError(f"Failed to send email: {str(e)}")



