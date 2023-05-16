import os
from typing import List
import requests
import json
import numpy as np


def check_filenames(path: str, pattern: str) -> np.ndarray:
    """
    Check if pattern is included in filenames in path. If yes, return indices of those filenames.
    Otherwise return empty array

    :param path: String. Path where to look for the filenames
    :param pattern: String. Pattern for which the filenames should be searched
    :return: result: numpy array. Either array of indices of the filenames that inclcude pattern, or an empty array
    """

    files = os.listdir(path)
    result = np.where([pattern in i for i in files])[0]
    return result


def download_weather_data(location: str, filepath: str) -> None:
    """
    Download forecast for 5 days in 3 hour intervals from openweathermap.org

    :param location: string. location name for which the forecast is requested
    :param filepath: path where the result is saved to
    :return:
    """
    api_address = "https://api.openweathermap.org/data/2.5/forecast?q=" + location + ",ger&appid=ca3c615c20062c4fed7b25374cb16a77"
    api_result = requests.get(api_address)
    with open(filepath, "w") as fp:
        json.dump(api_result.json(), fp)


def kelvin_to_celsius(deg_k: float) -> float:
    """ Converts a float from kelvin to celsius scale"""
    deg_c = deg_k - 273.15
    return deg_c


def extract_vals_from_dict(d: dict) -> [List, List, List, List]:
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
