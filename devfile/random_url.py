import random
from datetime import datetime, timedelta

# Function to generate a random upload URL
def generate_upload_url():
    # Random date and time generation
    base_time = datetime(2024, 12, 23, 12, 30, 45)
    random_time = base_time + timedelta(minutes=random.randint(1, 1000))
    
    # Generate random sensor data values
    temp = round(random.uniform(20.0, 30.0), 1)
    hum = round(random.uniform(50.0, 80.0), 1)
    soil_temp = round(random.uniform(15.0, 25.0), 1)
    soil_humidity = round(random.uniform(30.0, 60.0), 1)
    soil_ph = round(random.uniform(5.0, 7.0), 1)
    soil_ec = random.randint(1000, 1500)
    input_ph = round(random.uniform(6.0, 7.0), 1)
    input_ec = random.randint(800, 1000)
    drain_ph = round(random.uniform(6.5, 7.5), 1)
    drain_ec = random.randint(800, 1000)
    plant_weight = round(random.uniform(10.0, 20.0), 1)
    input_weight = round(random.uniform(10.0, 20.0), 1)
    drain_weight = round(random.uniform(5.0, 10.0), 1)

    # Format the time for the URL
    formatted_time = random_time.strftime("%Y-%m-%d %H:%M:%S")
    
    # Generate the URL
    url = f"http://127.0.0.1:8000/upload/{formatted_time}/{temp}/{hum}/{soil_temp}/{soil_humidity}/{soil_ph}/{soil_ec}/{input_ph}/{input_ec}/{drain_ph}/{drain_ec}/{plant_weight}/{input_weight}/{drain_weight}/"
    
    return url

# Generate 20 random URLs
random_urls = [generate_upload_url() for _ in range(20)]
random_urls
