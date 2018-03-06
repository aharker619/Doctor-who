import requests
from math import sqrt, pow

def temp_description(zip_code):
    '''
    Given a zip code, returns the current temperature in celcius,
        and a description of the weather outside
        
    Input: zip_code (integer, or string)
    
    Return: (description, temp_celcius)
        description: description of weather (string)
        temp_celsius: temperature in celcius (string)
        
    Exception:
        if zip_code not in USA, then returns (-1, -1)
    '''
    zip_code = str(zip_code)
    api_key = '3f180d31de6b4b363583654168714937'
    link = ('http://api.openweathermap.org/data/2.5/weather?appid=' + api_key +
            '&zip=' + zip_code)
    json_data = requests.get(link).json()
    description = []
    if len(json_data) > 2:
        desc_code = json_data['weather'][0]['id']
        extreme_codes = [202, 212, 221, 504, 511, 522, 602, 611, 900, 901, 
                         902, 903, 904, 905, 906, 959, 960, 961, 962]
        if desc_code in extreme_codes:
            description.append(json_data['weather'][0]['description'])

        temp_f = (9 / 5 * (json_data['main']['temp'] - 273.15)) + 32
        wind_mph = json_data['wind']['speed'] * 2.23694
        
        if temp_f >= 80:
            humidity = json_data['main']['humidity']
            heat_index = calc_heat_index(temp_f, humidity)
            if heat_index >= 105:
                heat_warning = "Heat advisory: the heat index is {}.".format(heat_index)
                description.append(heat_warning)
        if temp_f <= 50 and wind_mph > 3:
            wind_chill = calc_wind_chill(temp_f, wind_mph)
            if wind_chill < -20:
                chill_warning = "Wind Chill advisory: the wind chill is {}.".format(wind_chill)
                description.append(chill_warning)
    
    return description


def calc_heat_index(temp_f, humidity):
    '''
    Calculate the heat index using the Rothfusz regression equation
    www.wpc.ncep.noaa.gov/html/heatindex_equation.shtml
    '''
    adj = 0
    heat_index = (-42.379 + 2.04901523 * temp_f + 10.14333127 * humidity - 
        0.22475541 * temp_f * humidity - 0.00683783 * temp_f * temp_f - 
        0.05481717 * humidity * humidity + 0.00122874 * temp_f * temp_f * 
        humidity + 0.00085282 * temp_f * humidity * humidity - 0.00000199 * 
        temp_f * temp_f * humidity * humidity)
   
    if humidity < 13 and temp_f < 112:
        adj = -1 * ((13 - humidity) / 4) * sqrt((17 - abs(temp_f - 95)) / 17)
    if humidity > 85 and temp_f < 87:
        adj = ((humidity - 85) / 10) * ((87 - temp_f) / 5)

    return heat_index + adj


def calc_wind_chill(temp_f, wind_mph):
    '''
    Calculate the wind chill
    www.weather.gov/media/epz/wxcalc/windChill.pdf
    '''
    wind_chill = 35.74 + (0.6215 * temp_f) - (35.75 * pow(wind_mph, 0.16)) + (
                 0.4275 * temp_f * pow(wind_mph, 0.16))

    return wind_chill


def alerts(zip_code):
    '''
    Given a zip_code, returns the number of alerts issued for that particular zip_code at the time,
        along with the alerts as a list.
        
    Input: zip_code (as integer or string)
    
    Result: returns a tuple of (the number of alerts, list of alerts (if any))
            If no alerts, returns (0, [])
            
    Total number of calls allowed per day through wunderground alerts api: 500
    '''
    
    zip_code = str(zip_code)
    api_key = 'd334c0dee519eb72'
    link = 'http://api.wunderground.com/api/' + api_key + '/alerts/q/' + zip_code + '.json'
    
    json_data = requests.get(link).json()
        
    alerts = []
    for row in json_data['alerts']:
        alerts.append(row['message'])
        
    return alerts


def check_weather(zip_code):
    '''
    Check for extreme weather, high heat index, low wind chill, 
    and weather alerts for a given zipcode
    '''
    current_weather = temp_description(zip_code)
    alert = alerts(zip_code)

    return current_weather + alert