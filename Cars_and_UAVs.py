# -*- coding: utf-8 -*-
"""
Purpose: To illustrate object inheritance using two vehicle types.  Completing
         the code and debugging it was assigned as homework.
         
Created on Fri Sep 16 05:16:16 2022
@author: welchsm
"""
# Import standard stuff
import numpy as np
from trips import Road_trip, Flight_plan
from vehicles import Car, UAV
"""***************************"""
"""       SYSTEM STUFF        """
"""***************************"""
# Make a superclass for vehicles
np.random.seed(0)
def main():

    # Trips
    length_trips = 10
    trips = [Road_trip(WayPoints= np.linspace(0, 30, length_trips), SpeedLims=np.random.rand(length_trips)*105,
                       Roughness=np.random.uniform(low=0.3, high=0.8, size=length_trips)),
             Flight_plan(WayPoints= np.linspace(0, 1, length_trips), Headwinds=np.random.rand(length_trips)*18),
             Road_trip(WayPoints= np.linspace(0, 300, length_trips), SpeedLims=np.random.rand(length_trips)*105,
                       Roughness=np.random.uniform(low=0.3, high=0.8, size=length_trips)),
             Flight_plan(WayPoints=np.linspace(0, 200, length_trips), Headwinds=np.random.rand(length_trips) * 18)]

             # Make Four Trips
    vehicle_list = [Car(Top_Speed=105.), UAV(Top_Speed=50., Battery_Charge=100, Range=80),Car(Top_Speed=105.), UAV(Top_Speed=20., Battery_Charge=1, Range=100)]

    for i, vehicle in enumerate(vehicle_list):
        vehicle.add_trip(trips[i])
        vehicle.Go()
        vehicle.reset()



# Run the program
if __name__=="__main__": main()