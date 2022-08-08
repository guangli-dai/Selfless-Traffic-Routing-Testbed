from abc import ABC, abstractmethod
import random
import os
import sys
from core.Util import *
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("No environment variable SUMO_HOME!")
import traci
import sumolib

STRAIGHT = "s"
TURN_AROUND = "t"
LEFT = "l"
RIGHT = "r"
SLIGHT_LEFT = "L"
SLIGHT_RIGHT = "R"

class LWRController(RouteController):
    """
    My implementation of the Lighthill-Whitham-Richards model treats a certain number of cars within a network like an
    interval. Through this, without requiring sensors in the network, the LWRController uses the PDE Conservation Law to
    determine whether there is a traffic jam/slowdown and thus makes decisions based on those observations.  

    """
    def make_decisions(self, vehicles, connection_info):

        local_targets = {}
        
        return 0

    # calculate the change in flow rate and density with a car acting as an interval 
    def del_density_flow(vehicle):


        calculate_density_flow(self, """vehicle value that's passed down""")


        return 0
    
    
    def calculate_density_flow(self, vehicle):
        
        # calculate the speed of the car behind

        # calculate the speed of the car in front

        # calculate the density of cars on a certain edge in a given mile
        edge_length = self.connection_info.edge_length_dict[current_edge]
        vehicle_count = self.connection_info.edge_vehicle_count[current_edge] - 1

        density = vehicle_count / edge_length
        # if needed, finded the length of the edge

        # first, calculate the del speed between vehicles and multiply by the k value

        # wait another second or millisecond --> do the following again

        return density_one, density_two, flow_rate_one, flow_rate_two

        # more possible ideas 
        # """ rely on previous vehicle info from for in loop to calculate  speed/velocity"""