from django.shortcuts import render, redirect
import pusher
from django.http import HttpResponse
from .models import Sensor, Reading
from .tasks import my_reading_feed
pusher_client = pusher.Pusher(
  app_id='955817',
  key='d81c82457c99baa54a66',
  secret='da7d1eb8b0261474d8aa',
  cluster='ap2',
  ssl=True
)
def test1(request):
    global pusher_client
    if 'test1' in request.POST:
        val =request.POST['val']
        print(val)
        pusher_client.trigger('my-channel1', 'my-event', {'message': str(val)})#let us map channel id with sensor id
    return render(request,'test1.html')
def test2(request):
    return render(request,'test2.html')
def main_page(request):
    return render(request,'main_page.html')
def add_sensor(request):
    if 'add' in request.POST:
        url = request.POST['url']
        location = request.POST['location']
        my_sensor = Sensor(url = url,location_name = location,active = True)
        my_sensor.save()
        my_sensor.channel = 'my-channel' + str(my_sensor.id)
        my_sensor.save()
        my_reading_feed(my_sensor.id,repeat=1,repeat_until=None)
        return render(request,'main_page.html')
    return render(request,'main_page.html')
def home_data(request):
    all_sensor = Sensor.objects.all()
    return render(request,'home_data.html',{'all_sensor':all_sensor})
def get_graph_reading(request,sensor_id):
    sen = Sensor.objects.get(id = sensor_id)
    all_reading = Reading.objects.filter(sensor = sen).order_by('-pk')[:50]
    coordinates = []
    for reading in all_reading:
        my_date_time = ""
        x = reading.time 
        print(x)
        my_date = str(x.date())
        temp = str(x.time())
        (my_time,y) = temp.split('.')
        my_date_time = my_date + " " + my_time
        print(my_date_time)
        print(reading.field1)
        coordinates.append({'date_time':my_date_time,'field':reading.field2})
    print(coordinates)
    return render(request,'graph.html',{'coordinates':coordinates})

# Create your views here.
