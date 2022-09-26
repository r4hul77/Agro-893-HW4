import unittest
from vehicles import UAV, Car
from trips import Road_trip, Flight_plan
import numpy as np
# Write Unit tests for the Car and UAV classes here.

class TestUAV(unittest.TestCase):
    def test_uav(self):
        drone = UAV(Top_Speed=50., Battery_Charge=100, Range=50)
        flight_plan = Flight_plan(WayPoints=np.linspace(0, 50, 50), Headwinds=np.full(50, 0))
        drone.add_trip(flight_plan)
        drone.Go()
        end = drone.log[-1]
        self.assertEqual(end[1], 50) # Check if the Drone made it to the end of the flight plan
        self.assertLessEqual(end[3], 50)  # Check if the Drone went faster than its top speed
        self.assertEqual(end[3], 50) #Check if the Drone did not go as fast as it could
        self.assertGreaterEqual(end[2], 0) #Check if the Drone used more energy than it had

    def test_uav_with_wind(self):
        drone = UAV(Top_Speed=55., Battery_Charge=100, Range=50)
        flight_plan = Flight_plan(WayPoints=np.linspace(0, 50, 50), Headwinds=np.full(50, 1))
        drone.reset()
        drone.add_trip(flight_plan) # Add the flight plan to the drone
        drone.Go()
        end = drone.log[-1]
        self.assertLess(end[1], 50) # Check if the Drone did not make it to the end of the flight plan as expected

# Unit Tests for Car class
class TestCar(unittest.TestCase):
    def test_car(self):
        car = Car(Top_Speed=105.)
        road_trip = Road_trip(WayPoints=np.linspace(0, 50, 50), SpeedLims=np.full(50, 100), Roughness=np.full(50, 0.5))
        car.reset()
        car.add_trip(road_trip)
        car.Go()
        end = car.log[-1]
        self.assertLessEqual(end[3], 100 * 1.60934 / 3.6) # Check For Top Speed
        self.assertEqual(end[3], 100 * 1.60934 / 3.6) # Check For Reaching Top Speed
        self.assertGreaterEqual(end[2], 0) # Check if car used more energy than it had




if __name__ == '__main__':
    unittest.main()
