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
    return switcher.get(argument, 0) 
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
        42:44 ,       
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
        73:28,
        74:27,
        75:27,
        76:26,
        77:26,
        78:26,
        79:25,
        80:25,
        81:25,
        82:24,
        83:24,
        84:24,
        85:24,
        86:23,
        87:23,
        88:23,
        89:22,
        90:22,
        91:22,
        92:21,
        93:21,
        94:20,
        95:19,
        96:19,
        97:19,
        98:18,
        99:18,
        100:18,
        101:17,


    } 
    return switcher.get(argument, 0)
def NO(argument): 
    switcher = { 
        0: 97,
        1: 96, 
        2: 95,
        3 : 90,
        4 : 70,
        5 : 65,
        6 : 60,
        7 : 58,
        8 : 56,
        9 : 53,
        10: 51,
        11 : 49,
        12 : 48,
        13: 46,
        14: 45,
        15:43,
        16 : 42,
        17 :40,
        18: 39,
        19: 38,
        20: 37,
        21: 36,
        22 : 36,
        23: 34,
        24: 33,
        25: 32,
        26 :31,
        27: 30,
        28: 29,
        29: 28,
        30: 27,
        31: 26,
        32:25,
        33: 24,
        34: 23,
        35: 22,
        36:21,
        37:20,
        38:19,
        39:18,
        40:18,
        41:17,
        42:16,        
        44:15,
        45:15,
        46:14,
        47:13,
        48:12,
        49:12,
        50:10,
        51:10,
        52:9,
        53:9,
        54:8,
        55:8,
        56:8,
        57:7,
        58:7,
        59:7,
        60:7,
        61:7,
        62:6,
        63:6,
        64:6,
        65:6,
        66:5,
        67:5,
        68:5,
        69:5,
        70:4,
        71:4,
        72:4,
        73:4,
        74:4,

    } 
    return switcher.get(argument, 0) 
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
        print("PH",b['pH'],0.11)
        print("NOx",(b['NOx']*100))
        e = round(float(b['pH']))
        f = round(float(b['NOx'])*100)
        print(e,f)
        p = PH(e)
        q= NO(f)
        print(p,q,"my numbers")
        my_wqi = (p* 0.11 + q* 0.1 + 0.1 * 81)* (0.67/0.31)
        if my_wqi >60:
            my_wqi = my_wqi
        else:
            my_wqi = my_wqi + 35
        pusher_client.trigger(cur_sensor.channel, 'my-event', {'NOx':b['NOx'],'temp':b['temp'],'TDS':b['TDS'],'turbidity':b['turbidity'],'pH':b['pH'],'fetched':str(fetched),'wqi':my_wqi })
        my_reading = Reading(sensor = cur_sensor,field1 = b['NOx'],field2=b['temp'],field3=b['TDS'],field4 =b['turbidity'],field5= b['pH'], wqi = my_wqi  )
        my_reading.save()
        print(b['temp'])
    else:
        time.sleep(10)


