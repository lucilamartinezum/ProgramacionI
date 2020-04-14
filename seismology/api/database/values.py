import time
from random import uniform, random, randint, uniform

def send_data():
    value_sensor = {
    'datetime': time.strftime(r"%Y-%m-%d %H:%M:%S", time.localtime()),
    'depth': randint(5,250) ,
    'magnitude': round(uniform(2.0,5.5), 1),
    'latitude': uniform(-180,180),
    'longitude': uniform(-90, 90)
    }

    return value_sensor