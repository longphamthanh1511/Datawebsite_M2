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
        'sun': [entry.sun for entry in data_chart],

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

        'soil_temperature2': [entry.soil_temperature2 for entry in data_chart],
        'soil_humidity2': [entry.soil_humidity2 for entry in data_chart],
        'soil_ph2': [entry.soil_pH2 for entry in data_chart],
        'soil_ec2': [entry.soil_EC2 for entry in data_chart],
        'input_ph2': [entry.input_ph2 for entry in data_chart],
        'input_ec2': [entry.input_ec2 for entry in data_chart],
        'drain_ph2': [entry.drain_ph2 for entry in data_chart],
        'drain_ec2': [entry.drain_ec2 for entry in data_chart],
        'plant_weight2': [entry.plant_weight2 for entry in data_chart],
        'input_weight2': [entry.input_weight2 for entry in data_chart],
        'drain_weight2': [entry.drain_weight2 for entry in data_chart],
    }

    latest_pic = Pic.objects.order_by('-timestamp').first()

    return render(request, 'index.html', {'data': data, 'chart_data': chart_data, 'latest_pic': latest_pic})

def upload_data(
    request, time, temperature, humidity, sun, 
    
    soil_temperature, soil_humidity, 
    soil_pH, soil_EC, input_ph, input_ec, drain_ph, drain_ec, 
    plant_weight, input_weight, drain_weight,

    soil_temperature2, soil_humidity2, 
    soil_pH2, soil_EC2, input_ph2, input_ec2, drain_ph2, drain_ec2, 
    plant_weight2, input_weight2, drain_weight2,

    flag

):
    try:
        # Convert fields to the appropriate types
        time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')  # Parse the time string
        temperature = float(temperature)
        humidity = float(humidity)
        sun = float(sun)

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

        soil_temperature2 = float(soil_temperature2)
        soil_humidity2 = float(soil_humidity2)
        soil_pH2 = float(soil_pH2)
        soil_EC2 = int(soil_EC2)
        input_ph2 = float(input_ph2)
        input_ec2 = int(input_ec2)
        drain_ph2 = float(drain_ph2)
        drain_ec2 = int(drain_ec2)
        plant_weight2 = float(plant_weight2)
        input_weight2 = float(input_weight2)
        drain_weight2 = float(drain_weight2)

        flag = int(flag)

        # Create a new data entry
        new_data = Data.objects.create(
            time=time,
            temperature=temperature,
            humidity=humidity,
            sun = sun,
            co2 = 0,
            prep_f1 = 0,
            prep_f2 = 0,
            prep_f3 = 0,
            prep_i1 = 0,
            prep_i2 = 0,
            prep_i3 = 0,

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
            drain_weight=drain_weight,

            soil_temperature2=soil_temperature2,
            soil_humidity2=soil_humidity2,
            soil_pH2=soil_pH2,
            soil_EC2=soil_EC2,
            input_ph2=input_ph2,
            input_ec2=input_ec2,
            drain_ph2=drain_ph2,
            drain_ec2=drain_ec2,
            plant_weight2=plant_weight2,
            input_weight2=input_weight2,
            drain_weight2=drain_weight2
        )

        if flag == 0:
            send_email(new_data)

        else :
            send_water_email(new_data)

        # Calculate remaining water
        remaining_water = request.session.get('remaining_water', TANK_CAPACITY)
        remaining_water -= input_weight
        remaining_water = max(remaining_water, 0)  # Prevent negative values

        # Update the session
        request.session['remaining_water'] = remaining_water

        # Check threshold and send a warning email
        if remaining_water < 500:  # Threshold value
            send_warning_email_refill(remaining_water)

        
        # Calculate remaining water
        drain_weights = request.session.get('drain_weights', 0)
        drain_weights += drain_weight

        # Update the session
        request.session['drain_weights'] = drain_weights

        # Check threshold and send a warning email
        if drain_weights > 2000:  # Threshold value
            send_warning_email_drain(drain_weights)

        # Send email with the latest data
        

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
    Sun: {data.sun} w/m2

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

    Soil Temperature 2: {data.soil_temperature2} °C
    Soil Humidity 2: {data.soil_humidity2} %
    Soil pH 2: {data.soil_pH2}
    Soil EC 2: {data.soil_EC2} µS/m
    Input pH 2: {data.input_ph2}
    Input EC 2: {data.input_ec2} µS/m
    Drain pH 2: {data.drain_ph2}
    Drain EC 2: {data.drain_ec2} µS/m
    Plant Weight 2: {data.plant_weight2} gram
    Input Weight 2: {data.input_weight2} gram
    Drain Weight 2: {data.drain_weight2} gram
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

def send_water_email(data):
    # Format the email content with the latest data
    subject = f"Plan was watered at {data.time}"
    message = f"""
    New data has been uploaded to the system:

    Time: {data.time}
    Temperature: {data.temperature} °C
    Humidity: {data.humidity} %
    Sun: {data.sun} w/m2

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

    Soil Temperature 2: {data.soil_temperature2} °C
    Soil Humidity 2: {data.soil_humidity2} %
    Soil pH 2: {data.soil_pH2}
    Soil EC 2: {data.soil_EC2} µS/m
    Input pH 2: {data.input_ph2}
    Input EC 2: {data.input_ec2} µS/m
    Drain pH 2: {data.drain_ph2}
    Drain EC 2: {data.drain_ec2} µS/m
    Plant Weight 2: {data.plant_weight2} gram
    Input Weight 2: {data.input_weight2} gram
    Drain Weight 2: {data.drain_weight2} gram
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

    # Store the last remaining water value in the session
    request.session['remaining_water'] = current_water

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
    # Fetch the refill time from the session, or set it to the earliest possible time
    last_drain_time = request.session.get('last_drain_time', None)
    if last_drain_time:
        last_drain_time = datetime.fromisoformat(last_drain_time)
    else:
        last_drain_time = Data.objects.earliest('time').time  # Get the earliest timestamp in the database

    # Fetch data points after the last refill time
    data = Data.objects.filter(time__gte=last_drain_time).order_by('-time')[:20]
    data = data[::-1]  # Reverse to chronological order

    # Initialize remaining water list
    drain_weights = []
    drain_tank_weight = 0

    for entry in data:
        drain_tank_weight += entry.drain_weight
        drain_weights.append(drain_tank_weight)  # Prevent negative values

    # Store the last drain water value in the session
    request.session['drain_weights'] = drain_tank_weight

    # Prepare chart data
    chart_data = {
        "labels": [entry.time.strftime('%m-%d %H:%M') for entry in data],
        "values": drain_weights,
        "threshold": DRAIN_TANK_CAPACITY  # The threshold for the alert
    }

    return render(request, 'drain_tank_chart.html', {'chart_data': chart_data})

def drain_tank(request):
    if request.method == "POST":
        # Get the user-provided refill time from the form
        drain_time = request.POST.get('drain_time')
        try:
            # Parse the user-provided time and store it in the session
            drain_time = datetime.fromisoformat(drain_time)
            request.session['last_drain_time'] = drain_time.isoformat()
        except ValueError:
            # Handle invalid date input
            return render(request, 'drain_tank.html', {'error': 'Invalid date format. Please use YYYY-MM-DD HH:MM'})

        return redirect('drain_tank_chart')  # Redirect back to the chart page

    return render(request, 'drain_tank.html')  # Render the form

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

def send_warning_email_refill(remaining_water):
    subject = "Tank Water Level Warning!!!"
    message = f"""
    The remaining water level has dropped below the threshold: {remaining_water} grams.
    Please refill the tank soon!!!
    """
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        ['thanhlongpham15112000@gmail.com'],
        fail_silently=False,
    )

def send_warning_email_drain(drain_weights):
    subject = "Drain Tank Level Warning!!!"
    message = f"""
    The drain water level has risen above the threshold: {drain_weights} grams.
    Please drain the tank soon!!!
    """
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        ['thanhlongpham15112000@gmail.com'],
        fail_silently=False,
    )

