import numpy as np

from trips import Road_trip, Flight_plan, Trip



class Vehicle(object):

    # This will be overloaded by __init__ routines
    # in all subclasses.  There is really no need for
    # it but it is included to illustrate the pattern
    def __init__(self):
        pass

    def add_trip(self, trip):
        self.Trip = trip

    def get_name(self):
        pass

    # Set up values for common features
    def set_Vehicle_attributes(self,
                               E_avail=0.,  # V, MJ,     ratio, energy remain.
                               E_capac=1.,  # P, MJ,     ratio, "full tank"
                               E_effic=1.,  # V, km/MJ,  ratio, "milage"
                               T_Speed=1.,  # P, km/ksec,ratio, TopSpeed
                               SE_args=()  # Extra arguments for vehicle-
                               # specific Speed_Efficiency
                               ):

        # Stuff depending on type of vehicle
        self.E_avail = E_avail
        self.E_capac = E_capac
        self.E_effic = E_effic
        self.T_Speed = T_Speed
        self.SE_args = SE_args

        # Stuff that is trip dependent
        self.Trip = None  # Either a Road_Trip or Flight_Plan object
        # that describes the trip characteristics
        self.loc = 0.  # Location from start of trip. V km interval
        self.i = 0  # Index of current segment
        self.log = []  # Log of vehicle

    # Replensish the vehicle's store of energy
    def ReEnergize(self):
        self.E_avail = self.E_capac

    # Run until can go no more
    def Go_until_No_Go(self, L0):

        # Check if we have a planned trip on file
        if self.Trip == None:
            raise Exception("No planned trip plan on file")

        # Specialized Euler integrator that runs until the vehicle
        # can go no further or the end of the travel plan is reached.
        # The returned values are the ending location and whether or
        # not (boolean) the travel plan finished.

        # Specify a small time step
        D_step = (self.Trip.WayPoints[-1] -  # Distance step
                  self.Trip.WayPoints[0]) / 100
        T_step = D_step / self.T_Speed  # Min time to go
        # that far
        # Starting position
        Loc = L0


        # Run until exhausted
        while self.E_avail > 0. and Loc < self.Trip.WayPoints[-1]:
            speed, efficiency = self.Trip.Speed_Efficiency(Loc, *self.SE_args)
            distance = speed * T_step  # (km/ksec)*ksec
            Loc += distance
            energy = distance / efficiency  # km/(km/MJ)
            self.E_avail -= energy
            self.i += 1
            # Log the trip
            self.log.append(np.array([self.i, Loc, self.E_avail, speed, efficiency]))


        # Return final location and if the travel is finished
        return Loc, Loc >= self.Trip.WayPoints[-1]

    # Subclass Car
    def reset(self):
        self.ReEnergize()
        self.Trip = None
        self.loc = 0

    def Go(self):
        self.loc, finished = self.Go_until_No_Go(self.loc)
        return finished

class Car(Vehicle):

    def get_name(self):
        return f"Car with milage {self.E_effic:.2f} km/MJ"

    # Create an instance
    def __init__(self,
                 Tank_Size=17.,  # P, ratio, gallons, "full tank"
                 HwyMilage=26.,  # P, ratio, mile/gal
                 Top_Speed=89.  # P, ratio, miles/hour
                 ):

        super().__init__()
        """ Convert units from Car to Vehicle """
        # (31.536 MJ/l petrol)*(3.78541 l/gal)*(tank size gal)
        FullTank = 31.536 * 3.78541 * Tank_Size
        # ((mile/gal)(1.60934 km/mile))/((3.78541 l/gal)(31.536 MJ/l petrol))
        Milage = (HwyMilage * 1.60934) / (3.78541 * 31.536)
        # (mi/hr)*(1.60934 km/mile)/(3.6 ksec/hr)
        T_Speed = Top_Speed * 1.60934 / 3.6

        # Store info in Vehicle units
        self.set_Vehicle_attributes(E_capac=FullTank,  # Full tank in J
                                    E_avail=FullTank,  # Start w/ full tank
                                    E_effic=Milage,  # "Milage" in km/MJ
                                    T_Speed=T_Speed,  # Top speed km/ksec
                                    SE_args=(Milage,))  # Speed_Efficiency args

        # Record that the car tank is full
        self.Tanks = 1  # V, unitless (pure number), ratio, tankfulls for trip

    # Take the trip
    def Go(self):

        # Burn the first tank
        self.loc, Arrived = self.Go_until_No_Go(self.loc)

        # Keep going if necessary
        while not Arrived:
            self.ReEnergize()
            self.Tanks += 1
            self.loc, Arrived = self.Go_until_No_Go(self.loc)

        # Output trip info
        print("Car trip completed with", self.Tanks, "tank needed")

    def add_trip(self, trip):
        if (isinstance(trip, Road_trip)):
            self.Trip = trip
        else:
            raise Exception("Car can't Fly can only take RoadTrip")




# Subclass UAV
class UAV(Vehicle):

    def get_name(self):
        return f"UAV with efficiency {self.E_effic:.1f} km/MJ"

    # Create an instance
    def __init__(self,
                 Battery_Charge=10.,  # P, ratio, Watt hours
                 Range=15.,  # P, ratio, km on full battery charge
                 Top_Speed=20.  # P, ratio, km/hr in still air
                 ):

        """Convert to Vehicle units;store with set_Vehicle_attributes"""
        super().__init__()
        self.max_battery_charge = Battery_Charge * 0.0036 # Watts hour to MJ
        self.Still_Air_Efficiency = Range / self.max_battery_charge
        self.set_Vehicle_attributes(E_capac=self.max_battery_charge,  # Full tank in MJ
                                    E_avail=self.max_battery_charge,  # Start w / full tank
                                    E_effic=self.Still_Air_Efficiency,  # "Still_Air_Efficiency" in km/MJ
                                    T_Speed=Top_Speed,  # Top speed km/ksec
                                    SE_args=(self.Still_Air_Efficiency, Top_Speed))



    # Fly the mission
    def Fly_Mission(self):

        # Burn the first tank
        self.loc, Arrived = self.Go_until_No_Go(self.loc)

        # Keep going if necessary
        while not Arrived and self.E_avail > 0.:
            print(self.E_avail)
            self.loc, Arrived = self.Go_until_No_Go(self.loc)

        # Did we crash?
        if self.E_avail <= 0.:
            print("Crashed and burned", self.loc, "km into the mission")
        elif Arrived:
            print("Mission completed")

    def add_trip(self, trip):
        # check if it is not a Flight_plan instance
        if  isinstance(trip, Flight_plan)==False:
            raise Exception("UAV can only take FlightPlan")

        # check if one of the trip headwind is bigger than the top speed
        for headwind in trip.Headwinds:
            if headwind > self.T_Speed:
                print(headwind, self.T_Speed)
                raise Exception("UAV can't fly in headwind bigger than top speed")
        self.Trip = trip

    def Go(self):
        self.Fly_Mission()

"""***************************"""
"""     ENVIRONMENT STUFF     """
"""***************************"""
# Describes a road trip and road conditions along the way
""" Example usage """
