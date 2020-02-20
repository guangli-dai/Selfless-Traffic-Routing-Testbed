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
    '''
    Base class for routing policy
    '''
    def __init(self, connection_info):
        self.connection_info = connection_info
        self.direction_choices = [STRAIGHT, TURN_AROUND,  SLIGHT_RIGHT, RIGHT, SLIGHT_LEFT, LEFT]
    @abstractmethod
    def make_decision(self, vehicle_id):
        pass

class RandomPolicy(RouteController):
    def __init__(self, connection_info):
        super().__init(connection_info)

    def make_decision(self, vehicle_id):
        return random.randint(0, 6)
