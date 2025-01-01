import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

class Weather:
  def __init__(self):
    # initialize the member variable
    self.data = None # (366, (day, temperature, wind_speed))
    self.data_seasonal = {}
    self.time = None
    self.temperature = None
    self.wind_speed = None
    self.idx_season_shift = [62, 123, 241, 336]
    # read the data from the file
    self.read_data()
    # sort the data by season
    self.sort_by_season()
    # calculate the average temperature and wind speed by season
    self.calculate_avg_by_season()


  def read_data(self):
    # read the data from the file
    raw_data = pd.read_excel("data/weather/weather.xls", engine="xlrd")
    # extract the date, temperature and wind speed
    datetime_strings = raw_data["Date"].values
    temperature = raw_data["T"].values
    wind_speed = raw_data["Ff"].values
    # convert the strings to datetime objects
    parsed_datetimes = [
      datetime.strptime(dt_str, "%d.%m.%Y %H:%M")
      for dt_str in datetime_strings
    ]
    # convert the datetime objects to integers
    date_smallest = min(parsed_datetimes)
    date_int = [
      (dt - date_smallest).days
      for dt in parsed_datetimes
    ]
    # merge the data by date and calculate the average
    data_avg_by_date = {}
    for i in range(len(date_int)):
      if date_int[i] not in data_avg_by_date:
        data_avg_by_date[date_int[i]] = [temperature[i], wind_speed[i], 1]
      else:
        data_avg_by_date[date_int[i]][0] += temperature[i]
        data_avg_by_date[date_int[i]][1] += wind_speed[i]
        data_avg_by_date[date_int[i]][2] += 1
    data_avg_by_date = {
      key: [value[0] / value[2], value[1] / value[2]]
      for key, value in data_avg_by_date.items()
    }
    key_arr = np.array(list(data_avg_by_date.keys())).reshape(-1,1)
    value_arr = np.array(list(data_avg_by_date.values()))
    self.data = np.append(key_arr, value_arr, axis=1)
    # sort the data by date
    sorted_indices = np.argsort(self.data[:, 0])
    self.data = self.data[sorted_indices]

  def sort_by_season(self):
    self.data_seasonal["spring"] = self.data[self.idx_season_shift[0]:self.idx_season_shift[1], :]
    self.data_seasonal["summer"] = self.data[self.idx_season_shift[1]:self.idx_season_shift[2], :]
    self.data_seasonal["fall"] = self.data[self.idx_season_shift[2]:self.idx_season_shift[3], :]
    self.data_seasonal["winter"] = np.append(self.data[:self.idx_season_shift[0], :], self.data[self.idx_season_shift[3]:, :], axis=0)

  def calculate_avg_by_season(self):
    self.temperature = {}
    self.wind_speed = {}
    for season in self.data_seasonal:
      self.temperature[season] = np.mean(self.data_seasonal[season][:, 1])
      self.wind_speed[season] = np.mean(self.data_seasonal[season][:, 2])
    

if __name__ == "__main__":
  w = Weather()