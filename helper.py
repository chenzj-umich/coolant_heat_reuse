import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class System:
  def __init__(self, temp_air, temp_water, wind_speed):
    # initialize the variables(temp, wind speed), constants, data repositories
    self.variables = {}
    self.constants = {}
    self.data_repo = {
      "nu": {"directory": "data/water_properties/kinematic_viscosity_e-6.csv", "scale": 1e-6},
      "k": {"directory": "data/water_properties/thermal_conductivity_e-3.csv", "scale": 1e-3},
      "alpha": {"directory": "data/water_properties/thermal_diffusivity_e-6.csv", "scale": 1e-6},
      "beta": {"directory": "data/water_properties/thermal_expansion_coefficient_e-3.csv", "scale": 1e-3}
    }
    # store variables in the class
    self.store_variables(temp_air, temp_water, wind_speed)
    # get the interpolated constants from the data repository under current condition
    self.interpolate_constants()
    # calculate the secondary constants
    self.calculate_constants()
    # calculate the secondary variables
    self.calculate_variables()
    # calculate the power transferred from the water to the air
    self.calculate_power()
    # calculate the total cost annually
    self.calculate_total_cost()


  def store_variables(self, temp_air, temp_water, wind_speed):
    # temperature_air, temperature_water, wind_speed, a, b
    self.variables["temperature_air"] = temp_air
    self.variables["temperature_water"] = temp_water
    self.variables["wind_speed"] = wind_speed

  def interpolate_constants(self):
    # nu, k, alpha, beta
    for var in self.data_repo:
      data = pd.read_csv(self.data_repo[var]["directory"])
      val = np.interp(self.variables["temperature_air"], data["temperature"], data[var]) * self.data_repo[var]["scale"]
      self.constants[var] = val

  def calculate_constants(self):
    self.constants["a"] = 40
    self.constants["b"] = 60
    self.constants["number_of_reserviors"] = 4
    self.constants["cost_per_kWh"] = 0.38
    self.constants["g"] = 9.81
    self.constants["Re_c"] = 5e5
    # calculate the primary constants
    self.calculate_A() # depends on a and b
    self.calculate_P() # depends on a and b
    self.calculate_L() # depends on A and P
    self.calculate_Pr() # depends on nu and alpha

  def calculate_variables(self):
    # natural convection
    self.calculate_Ra_nc() # depends on g, beta, L, nu, alpha, temperature_air, and temperature_water
    self.calculate_Nu_nc() # depends on Ra
    self.calculate_h_nc() # depends on Nu

    # forced convection
    self.calculate_Re_fc() # depends on wind_speed, L and nu
    self.calculate_Nu_fc() # depends on Re and Pr
    self.calculate_h_fc() # depends on Pr and Re

    # combined convection
    self.calculate_h_combined() # depends on h_nc and h_fc

    # # print the results
    # print(self.variables)
    # print("h_nc:\t", self.variables["h_nc"])
    # print("h_fc:\t", self.variables["h_fc"])
    # print("h:\t", self.variables["h"])


  # ------------------- Primary constants -------------------
  def calculate_A(self):
    self.constants["a"] = self.constants["a"] * self.constants["b"]
  
  def calculate_P(self):
    self.variables["P"] = 2 * (self.constants["a"] + self.constants["b"])

  def calculate_L(self):
    self.variables["L"] = self.constants["a"] / self.variables["P"]

  def calculate_Pr(self):
    self.constants["Pr"] = self.constants["nu"] / self.constants["alpha"]

  # ------------------- Secondary constants -------------------
    # natural convection
  def calculate_Ra_nc(self):
    self.variables["Ra_nc"] = self.constants["g"] * self.constants["beta"] * (self.variables["temperature_water"] - self.variables["temperature_air"]) * self.variables["L"]**3 / (self.constants["nu"] * self.constants["alpha"])

  def calculate_Nu_nc(self):
    if self.variables["Ra_nc"] < 1e-7:
      self.variables["Nu_nc"] = 0.54 * self.variables["Ra_nc"]**(1/4)
    else:
      self.variables["Nu_nc"] = 0.15 * self.variables["Ra_nc"]**(1/3)

  def calculate_h_nc(self):
    self.variables["h_nc"] = self.variables["Nu_nc"] * self.constants["k"] / self.variables["L"]

    # forced convection
  def calculate_Re_fc(self):
    self.variables["Re_fc"] = self.variables["wind_speed"] * self.variables["L"] / self.constants["nu"]

  def calculate_Nu_fc(self):
    if self.variables["Re_fc"] < self.constants["Re_c"]:
      self.variables["Nu_fc"] = 0.664 * self.variables["Re_fc"]**(1/2) * self.constants["Pr"]**(1/3)
    else:
      self.variables["Nu_fc"] = (0.037 * self.variables["Re_fc"]**(4/5) - 871) * self.constants["Pr"]**(1/3)

  def calculate_h_fc(self):
    self.variables["h_fc"] = self.variables["Nu_fc"] * self.constants["k"] / self.variables["L"]

    # combined convection
  def calculate_h_combined(self):
    self.variables["h"] = (self.variables["h_nc"]**(7/2) + self.variables["h_fc"]**(7/2))**(2/7)

  def calculate_power(self):
    self.variables["power"] = self.variables["h"] * self.constants["a"] * (self.variables["temperature_water"] - self.variables["temperature_air"]) * self.constants["number_of_reserviors"]

  def calculate_total_cost(self):
    self.variables["cost_annually"] = self.variables["power"] / 1000 * 24 * 365 * self.constants["cost_per_kWh"]


def plot_annual_cost():
  temp_air_arr = np.linspace(-20, 30, 100)
  wind_speed_arr = np.linspace(0, 10, 100)
  T, u = np.meshgrid(temp_air_arr, wind_speed_arr)
  cost = np.zeros_like(T)
  for i in range(cost.shape[0]):
    for j in range(cost.shape[1]):
      sys = System(temp_air=T[i, j], temp_water=30, wind_speed=u[i, j])
      # print(temp_air_arr[i], wind_speed_arr[j], sys.variables["cost_annually"])
      cost[i, j] = sys.variables["cost_annually"]

  fig = plt.figure()
  ax = fig.add_subplot(111, projection='3d')
  surface = ax.plot_surface(T, u, cost, cmap='viridis', edgecolor='none')
  fig.colorbar(surface, shrink=0.5, aspect=5, label='Z value')

  # Axis labels
  ax.set_xlabel('Air temperature')
  ax.set_ylabel('Wind speed')
  ax.set_zlabel('Annual cost')

  # (Optional) Set a title
  ax.set_title('Annual cost as a function of air temperature and wind speed')

  plt.show()


if __name__ == "__main__":
  plot_annual_cost()