import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from heat_transfer import System, get_power
from weather import Weather


def info_seasonal():
  seasons = ["spring", "summer", "fall", "winter"]
  weather = Weather()
  for i in range(4):
    temp_air = weather.temperature[seasons[i]]
    wind_speed = weather.wind_speed[seasons[i]]
    power = get_power(temp_air, wind_speed)
    days = weather.data_seasonal[seasons[i]].shape[0]
    print(f"{seasons[i]}:\t\t{days}\t\tdays")
    print(f"Temperature:\t{temp_air:.2f}\t\t°C")
    print(f"Wind speed:\t{wind_speed:.2f}\t\tm/s")
    print(f"Power:\t\t{power:.2e}\tkW\n")


if __name__ == "__main__":
  info_seasonal()