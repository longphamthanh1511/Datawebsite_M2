from django.db import models

# Create your models here.
class Data(models.Model):
    time = models.DateTimeField()  
    temperature = models.FloatField()  
    humidity = models.FloatField()  
    soil_temperature = models.FloatField()  
    soil_humidity = models.FloatField()  
    soil_pH = models.FloatField()  
    soil_EC = models.IntegerField()
    input_ph = models.FloatField()  
    input_ec = models.IntegerField()
    drain_ph = models.FloatField()  
    drain_ec = models.IntegerField()    
    plant_weight = models.FloatField()
    input_weight = models.FloatField()
    drain_weight = models.FloatField()

class Pic(models.Model):
    # Field to store the uploaded image
    image = models.ImageField(upload_to='uploaded_images')
    timestamp = models.DateTimeField(auto_now_add=True)


    
