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

    # UAV unit tests
    print("\nStarting UAV unit tests...\n")

    print("Testing UAV with no wind in flight plan, and fuel capacity to just finish trip...\n")
    drone = UAV(Top_Speed=50., Battery_Charge=100, Range=50)
    flight_plan = Flight_plan(WayPoints=np.linspace(0, 50, length_trips), Headwinds=np.full(length_trips, 0))
    drone.add_trip(flight_plan)
    drone.Go()
    end = drone.log[-1]
    print(["%0.2f" % i for i in end])
    if end[1] < 50:
        print("The drone did not make it to the end of the flight plan.")
    elif end[3] > 50:
        print("The drone went faster than its top speed.")
    elif end[3] < 50:
        print("The drone did not go as fast as it could.")
    elif round(end[2],3) < 0:
        print("The drone used more energy than it had.")
    elif round(end[2],3) > 0:
        print("The drone did not use all of its energy.")
    else:
        print("The drone flew perfectly.\n")

    drone = UAV(Top_Speed=55., Battery_Charge=100, Range=50)
    flight_plan = Flight_plan(WayPoints=np.linspace(0, 50, length_trips), Headwinds=np.full(length_trips, 45))

    print("\nTesting the same UAV with wind in the flight plan, and fuel capacity for a no wind day...\n")
    drone.reset()
    drone.add_trip(flight_plan)
    drone.Go()
    end = drone.log[-1]
    if end[1] < 50:
        print("The drone did not make it to the end of the flight plan as expected.")
    elif end[1] >= 50:
        print("The drone made it further than expected. There is an error in the code.")

    #Car unit tests
    print("\nStarting Car unit tests...\n")

    car = Car(Top_Speed=105.)
    road_trip = Road_trip(WayPoints=np.linspace(0, 50, length_trips), SpeedLims=np.full(length_trips, 100), Roughness=np.full(length_trips, 0.5))

    print("Testing car with 0.5 roughness in road trip, and fuel capacity to just finish trip...\n")
    car.reset()
    car.add_trip(road_trip)
    car.Go()
    end = car.log[-1]
    print(["%0.2f" % i for i in end])
    if end[1] < 50:
        print("The car did not make it to the end of the road trip.")
    elif end[3] > 100 * 1.60934 / 3.6:
        print("The car went faster than its top speed.")
    elif end[3] < 100 * 1.60934 / 3.6:
        print("The car did not go as fast as it could.")
    elif round(end[2],3) < 0:
        print("The car used more energy than it had.")
    else:
        print("The car drove perfectly.\n")





# Run the program
if __name__=="__main__": main()