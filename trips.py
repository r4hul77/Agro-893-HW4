import numpy as np


class Trip(object):

    def __init__(self):
        self.start = None
        self.end = None
        self.way_points = None
        self.time = None
        self.speed = None
        self.distances = None

    def set_start(self, start):
        self.start = start

    def set_end(self, end):
        self.end = end


    def set_way_points(self, way_points):
        self.way_points = way_points
        self.distances = np.cumsum(way_points)

    def run(self):
        pass

    def get_idx(self, loc):
        idx = np.searchsorted(self.distances, loc)
        return min(idx, len(self.distances) - 1)


class Road_trip(Trip):

    # Create a trip
    def __init__(self,
                 WayPoints,  # P, Successive intersections, interval, miles
                 SpeedLims,  # P, Speed limits on each segment, mi/hr
                 Roughness  # P, [.3 - .95], road roughness, unitless
                 #    reduces efficiency, ratio
                 ):

        super().__init__()

        self.set_way_points(WayPoints)
        self.set_start(WayPoints[0])
        self.set_end(WayPoints[-1])
        # Error check inputs - one should ALWAYS do
        if len(WayPoints) != len(Roughness) or \
                len(Roughness) != len(SpeedLims):
            raise Exception("Unequal sized Waypoint, SpeedLims, Roughness arrays")
        if np.min(Roughness) < 0.3 or np.max(Roughness) > 0.95:
            raise Exception("Roughness values must be between0.30 and 0.95")

        # Store the values after converting to Vehicle units
        # Waypoints*(1.60934 km/mi)
        self.WayPoints = WayPoints * 1.60934
        # (mi/hr)*(1.60934 km/mi)/(3.6 ksec/hr)
        self.SpeedLimits = SpeedLims * 1.60934 / 3.6
        self.Roughness = Roughness

    # Determine speed and efficiency at a point along the way
    def Speed_Efficiency(self, Loc, E_effic):
        """ Find which interval Loc is in so that you can set the
            speed to that interval's speed limit and the efficiency
            to E_effic * that interval's Roughness.             """

        """ Here is placeholder code until you get that done.  It 
            assumes that Loc falls in the first interval         """
        idx = self.get_idx(Loc)
        Speed = self.SpeedLimits[idx]  # Use the interval's speed limit
        Efficiency = E_effic * self.Roughness[idx]  # Use self.E_effic * Roughness

        # Done
        return Speed, Efficiency


# Describes a desired flight and the conditions encountered on the way
class Flight_plan(Trip):

    # Create a trip
    def __init__(self,
                 WayPoints,  # P, Successive waypoints, interval, km
                 Headwinds  # P, km/ksec, ratio, reduces speed
                 ):
        # Error check inputs - one should ALWAYS do
        if len(WayPoints) != len(Headwinds):
            raise Exception("Unequal number of waypoints and headwind values")

        # Store the values
        self.WayPoints = WayPoints
        self.Headwinds = Headwinds

        # Determine speed and efficiency at a point along the way based on

    # the headwinds and the top speed of the UAV in still air.  NOTE
    # that the number of arguments for Speed_Efficiency differs by
    # vehicle type.  That's why the superclass uses the SE_args tuple
    # as was used in class to pass different numbers of arguments to
    # the rhs routines for differential equation solving.
    def Speed_Efficiency(self, Loc, Still_Air_Efficiency, T_speed):
        # Determine the headwind by linear interpolation
        headwind = np.interp(Loc, self.WayPoints, self.Headwinds)
        # Determine the ground speed, which is the actual speed that
        # counts toward completion of the mission.  NOTE that if the
        # the headwind were faster than the top speed of the UAV in
        # still air, then the ground Speed would be negative.  Does
        # this code behave appropriately in this situation?  No it
        # does not.  That is called a design flaw.  Of course, does
        # one really want to be flying a UAV under conditions where
        # it can only go downwind?  Probably not.
        Speed = T_speed - headwind

        # The efficiency per distance traveled needs to be prorated by
        # the actual speed vs. the speed in still air.  That is, a
        # stong headwind will make the energy expenditure per unit
        # distance traveled over the ground quite large.

        Efficiency = max(0.0001, Still_Air_Efficiency * (Speed / T_speed))
        # Done
        return Speed, Efficiency

