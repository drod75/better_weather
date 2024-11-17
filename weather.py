import openmeteo_requests
import requests_cache
import pandas as pd
from pprint import pprint
from retry_requests import retry
from geopy.geocoders import Nominatim

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

urls = [
    "https://api.open-meteo.com/v1/forecast",
    "https://marine-api.open-meteo.com/v1/marine",
    "https://flood-api.open-meteo.com/v1/flood",
    "https://air-quality-api.open-meteo.com/v1/air-quality"
]

#daily
forecast_params  = ['temperature_2m_max', 'temperature_2m_min', 'apparent_temperature_max', 'apparent_temperature_min', 'precipitation_sum', 'rain_sum', 'showers_sum', 'precipitation_hours', 'precipitation_probability_mean', 'sunrise', 'sunset', 'wind_speed_10m_max', 'wind_gusts_10m_max', 'wind_direction_10m_dominant']
marine_params  = ['wave_height_max', 'wind_wave_height_max', 'swell_wave_height_max', 'wave_direction_dominant', 'wind_wave_direction_dominant', 'swell_wave_direction_dominant', 'wave_period_max', 'wind_wave_period_max', 'swell_wave_period_max', 'wind_wave_peak_period_max', 'swell_wave_peak_period_max']
air_params = ['carbon_monoxide', 'carbon_dioxide', 'ammonia', 'methane', 'dust', 'us_aqi']
flood_params  = ['river_discharge', 'river_discharge_mean', 'river_discharge_median', 'river_discharge_max', 'river_discharge_min']

#data parameters
web_params = [forecast_params, marine_params, flood_params, air_params]

def to_dict(idx, data):
    dct = dict()
    if data == None:
        return
    for l, item in enumerate(web_params[idx]):
        dct[item] = data.Variables(l).ValuesAsNumpy()
    return dct

def to_df(idx, data):
    df = pd.DataFrame(data)
    return df

def get_city_health(city_name):
    city_health = dict()
    geolocator = Nominatim(user_agent="Your_Name")
    location = geolocator.geocode(city_name)
    cords = {
        'lat': location.latitude,
        'lon': location.longitude
    }

    city_health.update({'city': city_name})

    for idx, url in enumerate(urls):
        params = {
            'latitude': cords['lat'],
            'longitude': cords['lon'],
            'timezone': 'auto',
            'daily': web_params[idx]
        }
        if idx == 0:
            params['temperature_unit'] = 'fahrenheit'
            params['wind_speed_unit'] = 'mph'
            params['precipitation_unit'] = 'inch'
        if idx == 2:
            params['forecast_days'] = 7

        responses = openmeteo.weather_api(url, params=params)
        response = responses[0]
        daily = response.Daily()
        data = to_dict(idx, daily)
        if data != None:
            df = to_df(idx, data)
            key = url.rsplit('/', 1)[1]
            city_health.update({key: df})

    return city_health
