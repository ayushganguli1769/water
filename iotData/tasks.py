from background_task import background
from iotData.models import Sensor, Reading
import random
import time
import pusher
import os,sys, firebase_admin
from firebase_admin import credentials, firestore,db
import ast
import datetime
dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
robo = os.path.join(dirname, "robo.json")
cred = credentials.Certificate(robo)
firebase_admin.initialize_app(cred)
db = firestore.client()
pusher_client = pusher.Pusher(
  app_id='955817',
  key='d81c82457c99baa54a66',
  secret='da7d1eb8b0261474d8aa',
  cluster='ap2',
  ssl=True
)
@background(schedule=1)
def my_reading_feed(cur_sensor_id):
    global db
    global pusher_client
    cur_sensor = Sensor.objects.get(id = cur_sensor_id)
    if cur_sensor.active:
        #key = '6UGVJGFVCvwOis1eJSjC'
        doc_ref = db.collection('tutorialfirebase-9ffa6').document(cur_sensor.url)
        doc = doc_ref.get()
        a =(u'{}'.format(doc.to_dict()))
        b = ast.literal_eval(a)
        print(b)
        x = str(b['temp'])
        fetched = datetime.datetime.now()
        pusher_client.trigger(cur_sensor.channel, 'my-event', {'NOx':b['NOx'],'temp':b['temp'],'TDS':b['TDS'],'turbidity':b['turbidity'],'fetched':str(fetched) })
        print(b['temp'])
    else:
        time.sleep(10)


