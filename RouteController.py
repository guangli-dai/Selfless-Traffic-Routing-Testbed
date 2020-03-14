from abc import ABC, abstractmethod
import random

from Util import *
import traci
import sumolib

STRAIGHT = "s"
TURN_AROUND = "t"
LEFT = "l"
RIGHT = "r"
SLIGHT_LEFT = "L"
SLIGHT_RIGHT = "R"

class RouteController(ABC):
    """
    Base class for routing policy

    To implement a scheduling algorithm, implement the make_decisions() method.
    Please use the boilerplate code from the example, and implement your algorithm between
    the 'Your algo...' comments.

    make_decisions takes in a list of vehicles and network information (connection_info).
        Using this data, it should return a dictionary of {vehicle_id: decision}, where "decision"
        is one of the directions defined by SUMO (see constants above). Any scheduling algorithm
        may be injected into the simulation, as long as it is wrapped by the RouteController class
        and implements the make_decisions method.

    :param connection_info: object containing network information, including:
                            - out_going_edges_dict {edge_id: {direction: out_edge}}
                            - edge_length_dict {edge_id: edge_length}
                            - edge_index_dict {edge_index_dict} keep track of edge ids by an index
                            - edge_vehicle_count {edge_id: number of vehicles at edge}
                            - edge_list [edge_id]

    """
    def __init__(self, connection_info):
        self.connection_info = connection_info
        self.direction_choices = [STRAIGHT, TURN_AROUND,  SLIGHT_RIGHT, RIGHT, SLIGHT_LEFT, LEFT]

    @abstractmethod
    def make_decisions(self, vehicles, connection_info):
        pass

class RandomPolicy(RouteController):
    """
    Example class for a custom scheduling algorithm.
    Utilizes a random decision policy until vehicle destination is within reach,
    then targets the vehicle destination.
    """
    def __init__(self, connection_info):
        super().__init__(connection_info)

    def make_decisions(self, vehicles, connection_info):
        """
        A custom scheduling algorithm can be written in between the 'Your algo...' comments.
        For each car in the vehicles batch, the wrapper code will loop your algorithm until:
            1) The decision is a valid one, AND
            2) The targeted edge is far enough away that TRACI will not take
               the vehicle out of the simulation before the vehicle has reached its true destination.
        :param vehicles: list of vehicles to make routing decisions for
        :param connection_info: object containing network information
        :return: decisions: {vehicle_id, decision}, where decision is one of "s", "l", etc (see constants at top of file)
        """

        # TODO make sure that the algorithm favors true destination edge if its in range
        decisions = {}
        for vehicle in vehicles:
            start_edge = vehicle.current_edge
            path_length = 0

            while True:
                '''
                Your algo starts here
                '''

                choice = self.direction_choices[random.randint(0, 6)]

                '''
                Your algo ends here
                '''
                if choice in self.connection_info.outgoing_edges_dict[start_edge].keys():
                    # if target edge is not long enough, continue, but use just calculated target edge as new current edge
                    path_length += \
                        self.edge_length_dict[self.connection_info.outgoing_edges_dict[start_edge][choice]]

                    # make sure vehicle won't exit TRACI prematurely by ensuring it doesn't
                    # reach the end of its TRACI destination edge before we catch it again.
                    # TODO how much time passes per time step? current_speed is m/s, so the below only works if time step is 1s
                    if path_length <= vehicle.current_speed:
                        start_edge = self.connection_info.outgoing_edges_dict[start_edge][choice]
                        continue

                    break

            decisions[vehicle.vehicle_id] = choice

        return decisions
