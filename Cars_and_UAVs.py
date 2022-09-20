# -*- coding: utf-8 -*-
"""
Purpose: To illustrate object inheritance using two vehicle types.  Completing
         the code and debugging it was assigned as homework.
         
Created on Fri Sep 16 05:16:16 2022
@author: welchsm
"""
# Import standard stuff
import numpy as np

"""***************************"""
"""       SYSTEM STUFF        """
"""***************************"""
# Make a superclass for vehicles
class Trip(object):

    def __init__(self):
        self.start = None
        self.end = None
        self.way_points = None
        self.time = None
        self.speed = None

    def set_start(self, start):
        self.start = start

    def set_end(self, end):
        self.end = end


    def set_way_points(self, way_points):
        self.way_points = way_points

    def run(self):
        pass

class Vehicle(object):
    
    # This will be overloaded by __init__ routines
    # in all subclasses.  There is really no need for
    # it but it is included to illustrate the pattern
    def __init__(self):
        pass

    def add_trip(self, trip):
        self.Trip = trip

    # Set up values for common features 
    def set_Vehicle_attributes(self,
                               E_avail=0., # V, MJ,     ratio, energy remain.
                               E_capac=1., # P, MJ,     ratio, "full tank"
                               E_effic=1., # V, km/MJ,  ratio, "milage"
                               T_Speed=1., # P, km/ksec,ratio, TopSpeed
                               SE_args=()  # Extra arguments for vehicle-
                                           # specific Speed_Efficiency
                               ):
        
        # Stuff depending on type of vehicle
        self.E_avail=E_avail
        self.E_capac=E_capac
        self.E_effic=E_effic
        self.T_Speed=T_Speed
        self.SE_args=SE_args
        
        # Stuff that is trip dependent
        self.Trip=None   # Either a Road_Trip or Flight_Plan object
                         # that describes the trip characteristics                 
        self.loc=0.      # Location from start of trip. V km interval
                                
    # Replensish the vehicle's store of energy
    def ReEnergize(self):
        self.E_avail=self.E_capac
    
    # Run until can go no more
    def Go_until_No_Go(self,L0):       
        
        # Check if we have a planned trip on file
        if self.Trip==None:
            raise Exception("No planned trip plan on file")

        # Specialized Euler integrator that runs until the vehicle
        # can go no further or the end of the travel plan is reached.
        # The returned values are the ending location and whether or
        # not (boolean) the travel plan finished.
            
        # Specify a small time step
        D_step=(self.Trip.WayPoints[-1]-       # Distance step
                self.Trip.WayPoints[ 0])/100
        T_step=D_step/self.T_Speed             # Min time to go
                                               # that far
        # Starting position
        Loc=L0
        
        # Run until exhausted
        while self.E_avail>0. and Loc<self.Trip.WayPoints[-1]:
            speed,efficiency=self.Trip.Speed_Efficiency(Loc,*self.SE_args)
            distance=speed*T_step        # (km/ksec)*ksec
            Loc+=distance
            energy=distance/efficiency   # km/(km/MJ)
            self.E_avail-=energy
        
        # Return final location and if the travel is finished
        return Loc,Loc>=self.Trip.WayPoints[-1]           

# Subclass Car        
class Car(Vehicle):
    
    # Create an instance
    def __init__(self,
                 Tank_Size=17., # P, ratio, gallons, "full tank"
                 HwyMilage=26., # P, ratio, mile/gal
                 Top_Speed=89.  # P, ratio, miles/hour
                 ):
                 
        """ Convert units from Car to Vehicle """
        # (31.536 MJ/l petrol)*(3.78541 l/gal)*(tank size gal)
        FullTank=31.536*3.78541*Tank_Size
        # ((mile/gal)(1.60934 km/mile))/((3.78541 l/gal)(31.536 MJ/l petrol))
        Milage=(HwyMilage*1.60934)/(3.78541*31.536)
        # (mi/hr)*(1.60934 km/mile)/(3.6 ksec/hr)
        T_Speed=Top_Speed*1.60934/3.6
        
        # Store info in Vehicle units
        self.set_Vehicle_attributes(E_capac=FullTank,   # Full tank in J
                                    E_avail=FullTank,   # Start w/ full tank
                                    E_effic=Milage,     # "Milage" in km/MJ
                                    T_Speed=T_Speed,    # Top speed km/ksec
                                    SE_args=(Milage,))  # Speed_Efficiency args

        # Record that the car tank is full
        self.Tanks=1   # V, unitless (pure number), ratio, tankfulls for trip
        
    # Take the trip
    def Car_Go(self):
        
        # Burn the first tank
        self.loc,Arrived=self.Go_until_No_Go(self.loc)
        
        # Keep going if necessary
        while not Arrived:
            self.ReEnergize()
            self.Tanks+=1
            self.loc,Arrived=self.Go_until_No_Go(self.loc)
            
        # Output trip info
        print("Car trip completed with",self.Tanks,"tank needed")

    def add_trip(self, trip):
        if(isinstance(trip, RoadTrip)):
            self.Trip = trip
        else:
            raise Exception("Car can't Fly can only take RoadTrip")
  

# Subclass UAV
class UAV(Vehicle):
    
    # Create an instance
    def __init__(self,
                 Battery_Charge=10., # P, ratio, Watt hours
                 Range=15.,          # P, ratio, km on full battery charge
                 Top_Speed=20.       # P, ratio, km/hr in still air
                 ):
        


        """Convert to Vehicle units;store with set_Vehicle_attributes"""
        pass  # Placeholder for you to fill in details.  In particular,
              # Battery_Charge         --->  E_capac
              # Battery_Charge         --->  E_avail
              # Battery_Charge & Range --->  E_effic
              # Top_Speed & E_effic    --->  SE_args
    
    # Fly the mission
    def Fly_Mission(self):
        
        # See how it goes
        EndPoint,MadeIt=self.Go_until_No_Go(self.loc)
        
        # Did we crash?
        if MadeIt:
            print("Mission completed")
        else:
            print("Crashed and burned",EndPoint,"km into the mission")

    def add_trip(self, trip):
        if(isinstance(trip, FlightPlan)):
            self.Trip = trip
        else:
            raise Exception("UAV can only take FlightPlan")

"""***************************"""
"""     ENVIRONMENT STUFF     """
"""***************************"""
# Describes a road trip and road conditions along the way
class Road_trip(Trip):
    
    # Create a trip
    def __init__(self,
                 WayPoints,     # P, Successive intersections, interval, miles
                 SpeedLims,     # P, Speed limits on each segment, mi/hr   
                 Roughness      # P, [.3 - .95], road roughness, unitless 
                                #    reduces efficiency, ratio
                 ):

        super().__init__()


        self.set_way_points(WayPoints)
        self.set_start(WayPoints[0])
        self.set_end(WayPoints[-1])
        # Error check inputs - one should ALWAYS do
        if len(WayPoints)!=len(Roughness) or\
           len(Roughness)!=len(SpeedLims):
            raise Exception("Unequal sized Waypoint, SpeedLims, Roughness arrays")
        if np.min(Roughness)<0.3 or np.max(Roughness)>0.95:
            raise Exception("Roughness values must be between0.30 and 0.95")
                
        # Store the values after converting to Vehicle units
        # Waypoints*(1.60934 km/mi)
        self.WayPoints=WayPoints*1.60934    
        # (mi/hr)*(1.60934 km/mi)/(3.6 ksec/hr)
        self.SpeedLimits=SpeedLims*1.60934/3.6 
        self.Roughness=Roughness
        
    # Determine speed and efficiency at a point along the way
    def Speed_Efficiency(self,Loc,E_effic):
        """ Find which interval Loc is in so that you can set the
            speed to that interval's speed limit and the efficiency
            to E_effic * that interval's Roughness.             """
        
        """ Here is placeholder code until you get that done.  It 
            assumes that Loc falls in the first interval         """
        Speed=self.SpeedLimits[0]             # Use the interval's speed limit
        Efficiency= E_effic* self.Roughness[0]# Use self.E_effic * Roughness
        
        # Done
        return Speed,Efficiency
        
        
# Describes a desired flight and the conditions encountered on the way        
class Flight_plan(Trip):
        
    # Create a trip
    def __init__(self,
                 WayPoints,     # P, Successive waypoints, interval, km
                 Headwinds      # P, km/ksec, ratio, reduces speed
                 ):

        # Error check inputs - one should ALWAYS do
        if len(WayPoints)!=len(Headwinds):
            raise Exception("Unequal number of waypoints and headwind values")
        
        # Store the values
        self.WayPoints=WayPoints    
        self.Headwinds=Headwinds 
        
    # Determine speed and efficiency at a point along the way based on
    # the headwinds and the top speed of the UAV in still air.  NOTE
    # that the number of arguments for Speed_Efficiency differs by
    # vehicle type.  That's why the superclass uses the SE_args tuple
    # as was used in class to pass different numbers of arguments to
    # the rhs routines for differential equation solving.
    def Speed_Efficiency(self,Loc,T_speed,Still_Air_Efficiency):
        
        # Determine the headwind by linear interpolation
        headwind=np.interp(Loc,self.WayPoints,self.Headwinds)
        
        # Determine the ground speed, which is the actual speed that
        # counts toward completion of the mission.  NOTE that if the
        # the headwind were faster than the top speed of the UAV in
        # still air, then the ground Speed would be negative.  Does
        # this code behave appropriately in this situation?  No it
        # does not.  That is called a design flaw.  Of course, does
        # one really want to be flying a UAV under conditions where
        # it can only go downwind?  Probably not.
        Speed=T_speed-headwind
        
        # The efficiency per distance traveled needs to be prorated by 
        # the actual speed vs. the speed in still air.  That is, a 
        # stong headwind will make the energy expenditure per unit
        # distance traveled over the ground quite large.
        Efficiency=Still_Air_Efficiency*(Speed/T_speed)
        
        # Done
        return Speed,Efficiency
        
""" Example usage """
def main():
    
    # Get a car
    My_Town_and_Country=Car(Top_Speed=105.)
    
    # Plan the trip
    WayPoints=np.array([0.,.5,1.5,10.])
    Roughness=np.array(4*[0.8])
    SpeedLimits=np.array([25.,25.,45.,75.])
    My_Town_and_Country.Trip=Road_trip(WayPoints,
                                       SpeedLimits,
                                       Roughness)
    
    # Take the trip
    My_Town_and_Country.Car_Go()
    
# Run the program
if __name__=="__main__": main()