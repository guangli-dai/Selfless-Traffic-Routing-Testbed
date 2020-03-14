import os
import sys
import optparse
from xml.dom.minidom import parse, parseString
from RouteController import *
from Util import *

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("No environment variable SUMO_HOME!")

from sumolib import checkBinary
import traci
import sumolib

"""
SUMO Selfless Traffic Routing (STR) Testbed
"""

MAX_SIMULATION_STEPS = 5000

STRAIGHT = "s"
TURN_AROUND = "t"
LEFT = "l"
RIGHT = "r"
SLIGHT_LEFT = "L"
SLIGHT_RIGHT = "R"

class StrSumo:
    def __init__(self, route_controller, connection_info):
        """
        :param route_controller: object that implements the scheduling algorithm for controlled vehicles
        """
        self.direction_choices = [STRAIGHT, TURN_AROUND, SLIGHT_RIGHT, RIGHT, SLIGHT_LEFT, LEFT]
        self.connection_info = connection_info
        self.route_controller = route_controller
        self.controlled_vehicles = self.get_controlled_vehicles() # dictionary of Vehicles by id

    def run(self):
        """
        Runs the SUMO simulation
        At each time-step, cars that have moved edges make a decision based on user-supplied scheduler algorithm
        Decisions are enforced in SUMO by setting the destination of the vehicle to the result of the
        :returns: total time, number of cars that reached their destination, number of deadlines missed
        """
        total_time = 0
        end_number = 0
        deadlines_missed = 0

        step = 0
        vehicles_to_direct = [] #  the batch of controlled vehicles passed to make_decisions()
        vehicle_IDs_in_simulation = []

        try:
            while traci.simulation.getMinExpectedNumber() > 0:
                vehicle_ids = set(traci.vehicle.getIDList())

                # store edge vehicle counts in connection_info.edge_vehicle_count
                self.get_edge_vehicle_counts()

                # iterate through vehicles currently in simulation
                for vehicle_id in vehicle_ids:

                    self.connection_info.edge_vehicle_count[traci.vehicle.getRoadID(vehicle_id)] += 1

                    # handle newly arrived controlled vehicles
                    if vehicle_id not in vehicle_IDs_in_simulation and vehicle_id in self.controlled_vehicles:
                        vehicle_IDs_in_simulation.append(vehicle_id)
                        traci.vehicle.setColor(vehicle_id, (255, 0, 0)) # set color so we cant visually track controlled vehicles

                    if vehicle_id in self.controlled_vehicles.keys():
                        current_edge = traci.vehicle.getRoadID(vehicle_id)

                        if current_edge not in self.connection_info.edge_index_dict.keys():
                            continue
                        elif current_edge == self.controlled_vehicles[vehicle_id].destination:
                            continue

                        if current_edge != self.controlled_vehicles[vehicle_id].current_edge:
                            self.controlled_vehicles[vehicle_id].current_edge = current_edge
                            self.controlled_vehicles[vehicle_id].current_speed = traci.vehicle.getSpeed(vehicle_id)
                            vehicles_to_direct.append(self.controlled_vehicles[vehicle_id])

                vehicle_decisions_by_id = self.route_controller.make_decisions(vehicles_to_direct, self.connection_info)

                for vehicle_id, decision in vehicle_decisions_by_id:
                    if decision not in self.connection_info.outgoing_edges_dict[self.controlled_vehicles[vehicle_id].current_edge]:
                        raise ValueError(f'{decision} does not lead to a valid edge from edge '
                                         f'{self.controlled_vehicles[vehicle_id].current_edge}')

                    current_edge_of_vehicle = self.controlled_vehicles[vehicle_id].current_edge
                    target_edge = self.connection_info.outgoing_edges_dict[current_edge_of_vehicle][decision]
                    traci.vehicle.changeTarget(vehicle_id, target_edge)


                arrived_at_destination = traci.simulation.getArrivedIDList()

                for vehicle_id in arrived_at_destination:
                    if vehicle_id in self.controlled_vehicles:
                        total_time += step - self.controlled_vehicles[vehicle_id].start_time
                        end_number += 1
                        if step > self.controlled_vehicles[vehicle_id].deadline:
                            deadlines_missed.append(vehicle_id)


                traci.simulationStep()
                step += 1

                if step > MAX_SIMULATION_STEPS:
                    break

        except ValueError as err:
            print(err)


        return total_time, end_number, deadlines_missed

    def get_edge_vehicle_counts(self):
        for edge in self.connection_info.edge_list:
            self.connection_info.edge_vehicle_count[edge] = traci.edge.getLastStepVehicleNumber(edge)

    #  This is a dummy method for getting vehicles; the vehicle generation code will provide the list of controlled vehicles in practice
    def get_controlled_vehicles(self):
        vehicle_list = {}

        #  just generate 1000 dummy vehicles for now...
        for i in range(1000):
            new_vehicle = Vehicle(i, "", 0, float('inf'))
            vehicle_list[i] = new_vehicle

        return vehicle_list


sumo_binary = checkBinary('sumo-gui')

# parse config file for map file name
dom = parse("myconfig.sumocfg")

net_file_node = dom.getElementsByTagName('net-file')
net_file_attr = net_file_node[0].attributes

net_file = net_file_attr['value'].nodeValue
init_connection_info = ConnectionInfo(net_file)

scheduler = RandomPolicy(init_connection_info)
simulation = StrSumo(scheduler, init_connection_info)



traci.start([sumo_binary, "-c", "myconfig.sumocfg",
             "--tripinfo-output", "trips.trips.xml", "--fcd-output", "testTrace.xml"])


total_time, end_number, deadlines_missed = simulation.Run()
print(str(total_time) + ' for ' + str(end_number) + ' vehicles.')
print(str(deadlines_missed +' deadlines missed.'))