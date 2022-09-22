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
    My_Town_and_Country.add_trip(Road_trip(WayPoints,
                                       SpeedLimits,
                                       Roughness))
    
    # Take the trip
    My_Town_and_Country.Car_Go()


    # Make Four Trips


# Run the program
if __name__=="__main__": main()