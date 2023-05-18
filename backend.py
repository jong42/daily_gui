import os
from typing import Tuple, List
import requests
import json
import numpy as np
import matplotlib.pyplot as plt


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
    api_address = (
        "https://api.openweathermap.org/data/2.5/forecast?q="
        + location
        + ",ger&appid=ca3c615c20062c4fed7b25374cb16a77"
    )
    api_result = requests.get(api_address)
    with open(filepath, "w") as fp:
        json.dump(api_result.json(), fp)


def kelvin_to_celsius(deg_k: float) -> float:
    """Converts a float from kelvin to celsius scale"""
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

    for entry in d["list"]:
        timestamp = entry["dt_txt"]
        temp = kelvin_to_celsius(entry["main"]["temp"])
        weather_status = entry["weather"][0]["description"]
        prec_prob = entry["pop"]

        timestamps.append(timestamp)
        temps.append(temp)
        weather.append(weather_status)
        prec_probs.append(prec_prob)

    return timestamps, temps, weather, prec_probs


def get_minmax_values(
    timestamps: List[str], temps: List[float]
) -> Tuple[List[str], List[float]]:
    """
    From two given lists of timestamps and values, extract the minimum and maximum value for each day and
    the corresponding timestamp

    :param timestamps: List of strings. The timestamps.
    :param temps: List of floats. The values from which to extract min and max values per day
    :return: minmax_timestamps: List of strings. list of timestamps corresponding to minmax_temps
             minmax_temps: List of floats. Minimum and Maximum value from temps for each day
    """
    minmax_timestamps = []
    minmax_temps = []
    unique_dates = np.unique([i[0:10] for i in timestamps])
    for date in unique_dates:
        # Get all data points corresponding to a given date
        sub_timestamp_indices = np.asarray([date in i for i in timestamps]).nonzero()[0]
        sub_timestamps = [timestamps[i] for i in sub_timestamp_indices]
        sub_temps = [temps[i] for i in sub_timestamp_indices]
        # Get exact timestamp and temperature for max and min temperature on that date
        max_temp = np.max(sub_temps)
        min_temp = np.min(sub_temps)
        max_temp_index = sub_temps.index(max_temp)
        min_temp_index = sub_temps.index(min_temp)
        max_temp_timestamp = sub_timestamps[max_temp_index]
        min_temp_timestamp = sub_timestamps[min_temp_index]
        # Add results to corresponding lists
        minmax_timestamps.append(max_temp_timestamp)
        minmax_timestamps.append(min_temp_timestamp)
        minmax_temps.append(max_temp)
        minmax_temps.append(min_temp)

        return minmax_timestamps, minmax_temps


def get_weather_symbols(weather: List[str], path: str) -> List:
    """
    create a list of images where each image is specified by its name in a list
    :param weather: list of strings. names of the image files
    :param path: string. path to the image files
    :return: symbols. List of Images. Has the same length as weather
    """
    paths = [os.path.join(path, weather_status + ".png") for weather_status in weather]
    symbols = [plt.imread(symbol_path) for symbol_path in paths]
    return symbols
