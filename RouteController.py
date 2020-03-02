from abc import ABC
from keras.models import load_model
import numpy as np
import random

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
    def __init(self, connection_info):
        self.connection_info = connection_info
        self.direction_choices = [STRAIGHT, TURN_AROUND,  SLIGHT_RIGHT, RIGHT, SLIGHT_LEFT, LEFT]

    @abstractmethod
    def make_decisions(self, vehicles, connection_info):
        pass

class RandomPolicy(RouteController):

    def __init__(self, connection_info):
        super().__init(connection_info)

    def make_decisions(self, vehicles, connection_info):
        decisions = {}
        for vehicle in vehicles:
            decisions[vehicle.vehicle_id] = self.direction_choices[random.randint(0, 6)]

        return decisions
