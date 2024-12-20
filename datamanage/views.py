from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from datetime import datetime
from .models import Data, Pic
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
from django.core.mail import EmailMessage
# Create your views here.


def index(request):
    # Fetch the 10 most recent entries, ordered by time (latest first)
    data = Data.objects.all().order_by('-time')[:10]

    # Fetch the most recent 20 entries, ordered by time (oldest first, for chart continuity)
    data_chart = Data.objects.all().order_by('-time')[:20]
    data_chart = data_chart[::-1]  # Reverse the queryset to arrange them by time moving forward
    
    # Prepare the data for all charts
    chart_data = {
        'labels': [entry.time.strftime('%m-%d %H:%M') for entry in data_chart],
        'temperature': [entry.temperature for entry in data_chart],
        'humidity': [entry.humidity for entry in data_chart],
        'soil_temperature': [entry.soil_temperature for entry in data_chart],
        'soil_humidity': [entry.soil_humidity for entry in data_chart],
        'soil_ph': [entry.soil_pH for entry in data_chart],
        'soil_ec': [entry.soil_EC for entry in data_chart],
        'input_ph': [entry.input_ph for entry in data_chart],
        'input_ec': [entry.input_ec for entry in data_chart],
        'drain_ph': [entry.drain_ph for entry in data_chart],
        'drain_ec': [entry.drain_ec for entry in data_chart],
        'plant_weight': [entry.plant_weight for entry in data_chart],
        'input_weight': [entry.input_weight for entry in data_chart],
        'drain_weight': [entry.drain_weight for entry in data_chart],
    }

    latest_pic = Pic.objects.order_by('-timestamp').first()

    return render(request, 'index.html', {'data': data, 'chart_data': chart_data, 'latest_pic': latest_pic})

def upload_data(
    request, time, temperature, humidity, soil_temperature, soil_humidity, 
    soil_pH, soil_EC, input_ph, input_ec, drain_ph, drain_ec, 
    plant_weight, input_weight, drain_weight
):
    try:
        # Convert fields to the appropriate types
        time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')  # Parse the time string
        temperature = float(temperature)
        humidity = float(humidity)
        soil_temperature = float(soil_temperature)
        soil_humidity = float(soil_humidity)
        soil_pH = float(soil_pH)
        soil_EC = int(soil_EC)
        input_ph = float(input_ph)
        input_ec = int(input_ec)
        drain_ph = float(drain_ph)
        drain_ec = int(drain_ec)
        plant_weight = float(plant_weight)
        input_weight = float(input_weight)
        drain_weight = float(drain_weight)

        # Create a new data entry
        new_data = Data.objects.create(
            time=time,
            temperature=temperature,
            humidity=humidity,
            soil_temperature=soil_temperature,
            soil_humidity=soil_humidity,
            soil_pH=soil_pH,
            soil_EC=soil_EC,
            input_ph=input_ph,
            input_ec=input_ec,
            drain_ph=drain_ph,
            drain_ec=drain_ec,
            plant_weight=plant_weight,
            input_weight=input_weight,
            drain_weight=drain_weight
        )

        # Send email with the latest data
        send_email(new_data)

        return JsonResponse({'status': 'success', 'message': 'Data uploaded and email sent successfully'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})





def send_email(data):
    # Format the email content with the latest data
    subject = f"New Data Upload at {data.time}"
    message = f"""
    New data has been uploaded to the system:

    Time: {data.time}
    Temperature: {data.temperature} °C
    Humidity: {data.humidity} %
    Soil Temperature: {data.soil_temperature} °C
    Soil Humidity: {data.soil_humidity} %
    Soil pH: {data.soil_pH}
    Soil EC: {data.soil_EC} µS/m
    Input pH: {data.input_ph}
    Input EC: {data.input_ec} µS/m
    Drain pH: {data.drain_ph}
    Drain EC: {data.drain_ec} µS/m
    Plant Weight: {data.plant_weight} gram
    Input Weight: {data.input_weight} gram
    Drain Weight: {data.drain_weight} gram
    """

    # Fetch the latest uploaded picture
    latest_pic = Pic.objects.order_by('-timestamp').first()

    # Prepare the email
    email = EmailMessage(
        subject,
        message,
        settings.EMAIL_HOST_USER,  # From email
        ['thanhlongpham15112000@gmail.com'],  # To email
    )

    # Attach the latest picture if it exists
    if latest_pic and latest_pic.image:
        image_path = latest_pic.image.path
        email.attach_file(image_path)

    # Send the email
    email.send(fail_silently=False)

    

TANK_CAPACITY = 5000

def tank_water_chart(request):
    # Fetch the refill time from the session, or set it to the earliest possible time
    last_refill_time = request.session.get('last_refill_time', None)
    if last_refill_time:
        last_refill_time = datetime.fromisoformat(last_refill_time)
    else:
        last_refill_time = Data.objects.earliest('time').time  # Get the earliest timestamp in the database

    # Fetch data points after the last refill time
    data = Data.objects.filter(time__gte=last_refill_time).order_by('-time')[:20]
    data = data[::-1]  # Reverse to chronological order

    # Initialize remaining water list
    remaining_water = []
    current_water = TANK_CAPACITY

    for entry in data:
        current_water -= entry.input_weight
        remaining_water.append(max(current_water, 0))  # Prevent negative values

    # Prepare chart data
    chart_data = {
        "labels": [entry.time.strftime('%m-%d %H:%M') for entry in data],
        "values": remaining_water,
    }

    return render(request, 'tank_water_chart.html', {'chart_data': chart_data})

def refill_tank(request):
    if request.method == "POST":
        # Get the user-provided refill time from the form
        refill_time = request.POST.get('refill_time')
        try:
            # Parse the user-provided time and store it in the session
            refill_time = datetime.fromisoformat(refill_time)
            request.session['last_refill_time'] = refill_time.isoformat()
        except ValueError:
            # Handle invalid date input
            return render(request, 'refill_tank.html', {'error': 'Invalid date format. Please use YYYY-MM-DD HH:MM'})

        return redirect('tank_water_chart')  # Redirect back to the chart page

    return render(request, 'refill_tank.html')  # Render the form

DRAIN_TANK_CAPACITY = 2000  # Set the threshold for the drain tank

def drain_tank_chart(request):
    # Fetch all drain data points (drain weight) ordered by time
    data = Data.objects.all().order_by('-time')[:20]  # Fetch the last 20 data points
    data = data[::-1]  # Reverse the data to show in chronological order
    
    # Initialize drain tank weight tracking
    drain_tank_weight = 0
    drain_weights = []  # To store the weight values for the chart

    for entry in data:
        drain_tank_weight += entry.drain_weight  # Add the drain weight to the tank
        drain_weights.append(min(drain_tank_weight, DRAIN_TANK_CAPACITY))  # Don't exceed the tank capacity

    # Prepare chart data
    chart_data = {
        "labels": [entry.time.strftime('%m-%d %H:%M') for entry in data],
        "values": drain_weights,
        "threshold": DRAIN_TANK_CAPACITY  # The threshold for the alert
    }

    return render(request, 'drain_tank_chart.html', {'chart_data': chart_data})

def drain_tank(request):
    # Reset drain tank weight to 0
    Data.objects.filter(drain_weight__gte=0).update(drain_weight=0)
    return redirect('drain_tank_chart')  # Redirect back to the drain tank chart page

def send_mail_page(request):
    context = {}

    if request.method == 'POST':
        address = request.POST.get('address')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if address and subject and message:
            try:
                send_mail(subject, message, settings.EMAIL_HOST_USER, [address])
                context['result'] = 'Email sent successfully'
            except Exception as e:
                context['result'] = f'Error sending email: {e}'
        else:
            context['result'] = 'All fields are required'
    
    return render(request, "mail.html", context)

@csrf_exempt

def upload_image(request):
    if request.method == 'POST':
        try:
            # Get raw binary data from the request body
            image_data = request.body

            # Generate a unique file name using timestamp
            file_name = f'image_{now().strftime("%Y%m%d%H%M%S")}.jpg'

            # Save the image to the database with correct path handling
            pic = Pic()
            pic.image.save(file_name, ContentFile(image_data), save=True)

            return JsonResponse({'status': 'success', 'message': f'Image saved as {file_name}', 'pic_id': pic.id})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)