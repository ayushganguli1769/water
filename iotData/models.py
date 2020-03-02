from django.db import models
class Sensor(models.Model):
    url = models.CharField(null = True,max_length=250,blank=True)#key
    location_name = models.CharField(null = True,max_length=250,blank=True)
    active = models.BooleanField(default= False)
    channel = models.CharField(null= True, blank= True, max_length= 130)
    def __str__(self):
        return "Sensor: " + self.location_name
class Reading(models.Model):
    sensor = models.ForeignKey(Sensor,on_delete= models.CASCADE, related_name="read")
    field1 = models.FloatField(default= 0)
    field2 = models.FloatField(default= 0)
    field3 = models.FloatField(default= 0)
    field4 = models.FloatField(default= 0)
    field5 = models.FloatField(default= 0)
    wqi = models.FloatField(default= 0)
    time = models.DateTimeField(auto_now_add= True)
    def __str__(self):
        return "Reading from " + self.sensor.location_name