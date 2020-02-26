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
    """
    def __init(self, connection_info):
        self.connection_info = connection_info
        self.direction_choices = [STRAIGHT, TURN_AROUND,  SLIGHT_RIGHT, RIGHT, SLIGHT_LEFT, LEFT]
    @abstractmethod
    def make_decisions(self, vehicles, vehicle_id):
        pass

class RandomPolicy(RouteController):
    """
    :param connection_info: object containing network information including

    """
    def __init__(self, connection_info):
        super().__init(connection_info)

    def make_decisions(self, vehicles, connection_info):
        decisions = {}
        for vehicle in vehicles:
            decisions[vehicle.vehicle_id] = self.direction_choices[random.randint(0, 6)]

        return decisions
