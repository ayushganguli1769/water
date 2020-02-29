from django.shortcuts import render, redirect
import pusher
from django.http import HttpResponse
from .models import Sensor
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
# Create your views here.
