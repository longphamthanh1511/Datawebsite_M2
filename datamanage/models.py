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
    input_ec = models.FloatField()  
    drain_ph = models.FloatField()  
    drain_ec = models.FloatField()    
    plant_weight = models.FloatField()
    input_weight = models.FloatField()
    drain_weight = models.FloatField()

    soil_temperature2 = models.FloatField()  
    soil_humidity2 = models.FloatField()  
    soil_pH2 = models.FloatField()  
    soil_EC2 = models.IntegerField()
    plant_weight2 = models.FloatField()
    input_weight2 = models.FloatField()
    drain_weight2 = models.FloatField()
    input_ph2 = models.FloatField()  
    input_ec2 = models.FloatField() 
    drain_ph2 = models.FloatField()  
    drain_ec2 = models.FloatField() 


    sun = models.FloatField()
    co2 = models.FloatField()
    prep_f1 = models.FloatField()
    prep_f2 = models.FloatField()
    prep_f3 = models.FloatField()
    prep_i1 = models.IntegerField()
    prep_i2 = models.IntegerField() 
    prep_i3 = models.IntegerField()   



class Pic(models.Model):
    # Field to store the uploaded image
    image = models.ImageField(upload_to='uploaded_images')
    timestamp = models.DateTimeField(auto_now_add=True)


    
