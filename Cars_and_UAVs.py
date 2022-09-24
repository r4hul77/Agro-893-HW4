# -*- coding: utf-8 -*-
"""
Purpose: To illustrate object inheritance using two vehicle types.  Completing
         the code and debugging it was assigned as homework.
         
Created on Fri Sep 16 05:16:16 2022
@author: welchsm
"""
# Import standard stuff
import numpy as np
import matplotlib.pyplot as plt
from trips import Road_trip, Flight_plan
from vehicles import Car, UAV

"""***************************"""
"""       SYSTEM STUFF        """
"""***************************"""
# Make a superclass for vehicles
np.random.seed(0)


def plot_vehicle(vehicle, filename):
    log_colums = np.transpose(np.array(vehicle.log))
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(log_colums[0], log_colums[1], label='Location', color='blue')
    ax.plot(log_colums[0], log_colums[3], label='Speed', color='green')
    plt.ylabel('Location (km)/Speed (km/ksec)')
    ax2= ax.twinx()
    ax2.set_ylabel('Energy (MJ)')
    ax2.plot(log_colums[0], log_colums[2], label='Energy', color='red')
    ax.legend(loc='upper right')
    ax2.legend(loc='lower right')
    plt.xlabel('Time')

    plt.title(vehicle.get_name())
    plt.savefig(filename)

def main():

    # Trips
    length_trips = 10
    trips = [Road_trip(WayPoints= np.linspace(0, 30, length_trips), SpeedLims=np.random.rand(length_trips)*105,
                       Roughness=np.random.uniform(low=0.3, high=0.8, size=length_trips)),
             Flight_plan(WayPoints= np.linspace(0, 20, length_trips), Headwinds=np.random.rand(length_trips)*18),
             Road_trip(WayPoints= np.linspace(0, 300, length_trips), SpeedLims=np.random.rand(length_trips)*105,
                       Roughness=np.random.uniform(low=0.3, high=0.8, size=length_trips)),
             Flight_plan(WayPoints=np.linspace(0, 80, length_trips), Headwinds=np.random.rand(length_trips) * 10)]

             # Make Four Trips
    vehicle_list = [Car(Top_Speed=105.), UAV(Top_Speed=30., Battery_Charge=100, Range=30),Car(Top_Speed=105.), UAV(Top_Speed=50., Battery_Charge=290, Range=100)]

    for i, vehicle in enumerate(vehicle_list):
        vehicle.add_trip(trips[i])
        initial_energy = vehicle.E_avail
        vehicle.Go()
        # Plot the vehicle log
        plot_vehicle(vehicle, str(i)+".png")
        vehicle.reset()


# Run the program
if __name__=="__main__": main()