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

def main():
    
    # Get a car
    My_Town_and_Country=Car(Top_Speed=105.)
    
    # Plan the trip
    WayPoints=np.array([0.,.5,1.5,10.])
    Roughness=np.array(4*[0.8])
    SpeedLimits=np.array([25.,25.,45.,75.])
    My_Town_and_Country.add_trip(Road_trip(WayPoints=np.linspace(0, 10),
                                       SpeedLims=np.random.rand(),
                                       Roughness=Roughness))
    
    # Take the trip
    My_Town_and_Country.Car_Go()
    # Trips
    length_trips = 30
    trips = [Road_trip(WayPoints= np.linspace(0, 30, length_trips), SpeedLims=np.random.rand(length_trips)*105,
                       Roughness=np.random.uniform(low=0.3, high=0.8, size=length_trips)),
             Flight_plan(WayPoints= np.linspace(0, 30, length_trips), SpeedLims=np.random.rand(length_trips)*105),
             Road_trip(WayPoints= np.linspace(0, 30, length_trips), SpeedLims=np.random.rand(length_trips)*105,
                       Roughness=np.random.uniform(low=0.3, high=0.8, size=length_trips)),
             Flight_plan(WayPoints=np.linspace(0, 30, length_trips), SpeedLims=np.random.rand(length_trips) * 105)]

             # Make Four Trips
    vehicle_list = [Car(Top_Speed=105.), UAV(Top_Speed=105., Battery_Charge=100, Range=100)]

    for i, vehicle in enumerate(vehicle_list):
        vehicle.add_trip(trips[i])
        vehicle.Go()
        vehicle.reset()



# Run the program
if __name__=="__main__": main()