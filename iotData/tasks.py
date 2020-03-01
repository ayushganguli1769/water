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
"""
####wqi calculation function
def PH(argument): 
    switcher = { 
        1: 0, 
        2: 2,
        3 : 4,
        4 : 9,
        5 : 27,
        6 : 55,
        7 : 88,
        8 : 84,
        9 : 49,
        10 : 20,
        11 : 8,
        12 : 3,
        13 : 0, 
    } 
    return switcher.get(argument, "nothing") 
def Turbidity(argument): 
    switcher = { 
        1: 96, 
        2: 93,
        3 : 90,
        4 : 87,
        5 : 84,
        6 : 81,
        7 : 80,
        8 : 80,
        9 : 78,
        10: 76,
        11 : 74,
        12 : 72,
        13: 70,
        14: 69,
        15:67,
        16 : 66,
        17 :65,
        18: 63,
        19: 62,
        20: 62,
        21: 62,
        22 : 59,
        23: 59,
        24: 58,
        25: 58,
        26 :56,
        27: 55,
        28: 54,
        29: 54,
        30: 53,
        31: 52,
        32:51,
        33: 51,
        34: 50,
        35: 49,
        36:48,
        37:47,
        38:46,
        39:46,
        40:45,
        41:44,
        42:44        
        44:44,
        45:43,
        46:41,
        47:41,
        48:40,
        49:40,
        50:39,
        51:38,
        52:38,
        53:38,
        54:37,
        55:36,
        56:35,
        57:35,
        58:36,
        59:34,
        60:33,
        61:33,
        62:31,
        63:33,
        64:31,
        65:31,
        66:31,
        67:30,
        68:30,
        69:29,
        70:29,
        71:29,
        72:28,
        73:,
        74:,
        75:,
        76:,
        77:,
        78:,
        79:,
        80:,
        81:,
        82:,
        83:,
        84:,
        85:,
        86:,
        87:,
        88:,
        89:,
        90:,
        91:,
        92:,
        93:,
        94:,
        95:,
        96:,
        97:,
        98:,
        99:,
        100:,
        101:


    } 
    return switcher.get(argument, "nothing") 
"""
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
        my_reading = Reading(sensor = cur_sensor,field1 = b['NOx'],field2=b['temp'],field3=b['TDS'],field4 =b['turbidity']  )
        my_reading.save()
        print(b['temp'])
    else:
        time.sleep(10)


