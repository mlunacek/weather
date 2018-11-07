import requests
import json
from metar import Metar
import pytz
from datetime import timezone

stations = ['KBJC', 'K0CO', 'KBDU', 'KEGE', 'KCCU']

def now():
    u = datetime.datetime.utcnow()
    return u.replace(tzinfo=timezone.utc).astimezone(tz=pytz.timezone("America/Denver")).strftime("%Y-%m-%d %H:%M:%S")

def get_wind_direction(obs):
    direction = []
    if obs.wind_dir:
        direction.append(obs.wind_dir.compass())
    
    if obs.wind_dir_from:
        direction.append(obs.wind_dir_from.compass())
        direction.append(obs.wind_dir_to.compass())
        
    return direction

def get_wind(obs):
    if obs.wind_speed is None:
        return 0
    return obs.wind_speed.value("mph")

def get_wind_gust(obs):
    if obs.wind_gust is None:
        return 0
    return obs.wind_gust.value("mph")

def get_pressure(obs):
    if obs.press is None:
        return 0
    return obs.press.value('mb')

def get_temperature(obs):
    if obs.temp is None:
        return 0
    return obs.temp.string("F")

def get_denver_time(obs):
    return obs.time.replace(tzinfo=timezone.utc).astimezone(tz=pytz.timezone("America/Denver")).strftime("%Y-%m-%d %H:%M:%S")

def create_json(obs):
    
    return {'name': obs.station_id,
            'time': get_denver_time(obs),
            'wind_direction': get_wind_direction(obs),
            'wind': get_wind(obs),
            'gust': get_wind_gust(obs),
            'pressure': get_pressure(obs),
            'temperature': get_temperature(obs),
           }


def read_station(name):
    url =  "http://tgftp.nws.noaa.gov/data/observations/metar/stations/{}.TXT".format(name)
    res = requests.get(url)
    if res.status_code == 200:
        for line in res.text.split('\n'):
            if line.startswith(name):
                obs = Metar.Metar(line)
                return create_json(obs)

if __name__ == "__main__":
      
    res = []
    for name in stations:
        res.append(read_station(name))
        
    print(json.dumps(res, indent=4))