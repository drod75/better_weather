import openmeteo_requests
import requests_cache
import pandas as pd
from pprint import pprint
from retry_requests import retry

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

#hourly
forecast_params  = ['temperature_2m', 'relative_humidity_2m', 'apparent_temperature', 'surface_pressure', 'cloud_cover'
                    ,'wind_speed_10m', 'wind_direction_10m', 'wind_gusts_10m', 'precipitation', 'precipitation_probability','rain']
marine_params  = ['wave_height', 'wave_direction', 'wave_period', 'wind_wave_peak_period', 'ocean_current_velocity', 'ocean_current_direction']

#daily
air_params = ['carbon_monoxide', 'carbon_dioxide', 'ammonia', 'methane', 'dust', 'us_aqi']
flood_params  = ['river_discharge', 'river_discharge_mean', 'river_discharge_median', 'river_discharge_max', 'river_discharge_min']

#data parameters
web_params = [forecast_params, marine_params, flood_params, air_params]

def get_city_health(city_name):
    location = None
    city_health = []
    for idx, url in enumerate(urls):
        if idx == 2 or idx == 3:
            params = {
                'latitude': location.latitude,
                'longitude': location.longitude,
                'timezone': 'auto',
                'daily': web_params[idx]
            }
            responses = openmeteo.weather_api(url, params=params)
            response = responses[0]
            daily = response.Daily()
            js = daily.__dict__
            wd = {(url.rsplit('/', 1)[1]): js}
            city_health.append(wd)
        else:
            params = {
                'latitude': location.latitude,
                'longitude': location.longitude,
                'timezone': 'auto',
                'hourly': web_params[idx]
            }
            responses = openmeteo.weather_api(url, params=params)
            response = responses[0]
            hourly = response.Hourly()
            js = hourly.__dict__
            wd = {(url.rsplit('/', 1)[1]): js}
            city_health.append(wd)

    return city_health
