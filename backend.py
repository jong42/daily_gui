
from typing import List

def kelvin_to_celsius(deg_k:float)->float:
    """ Converts a float from kelvin to celsius scale"""
    deg_c = deg_k - 273.15
    return deg_c

def extract_vals_from_dict(d:dict) -> [List,List,List,List]:
    """
    Extract data on time stamps, temperature, weather status and precipitation probability from dictionary downloaded
    from openweathermap
    :param d: dictionary
    :return:
        timestamps: list of timestamps
        temps: list of temperature values
        weather_status: list of weather status values
        prec_probs: list of precipitation probabilities
    """

    timestamps = []
    temps = []
    weather = []
    prec_probs = []

    for entry in d['list']:
        timestamp = entry['dt_txt']
        temp = kelvin_to_celsius(entry['main']['temp'])
        weather_status = entry['weather'][0]['description']
        prec_prob = entry['pop']

        timestamps.append(timestamp)
        temps.append(temp)
        weather.append(weather_status)
        prec_probs.append(prec_prob)

    return timestamps, temps, weather, prec_probs