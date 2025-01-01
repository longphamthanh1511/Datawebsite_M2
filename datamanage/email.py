from django.core.mail import EmailMessage
from django.conf import settings
from .models import Data, Pic


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