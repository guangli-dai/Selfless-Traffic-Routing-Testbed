import os
import sys
import optparse
from xml.dom.minidom import parse, parseString
from core.Util import *
from core.target_vehicles_generation_protocols import *

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("No environment variable SUMO_HOME!")

import traci
import sumolib
from controller.RouteController import *

"""
SUMO Selfless Traffic Routing (STR) Testbed
"""

MAX_SIMULATION_STEPS = 2000

# TODO: decide which file to put these in. Right now they're also defined in RouteController!!
STRAIGHT = "s"
TURN_AROUND = "t"
LEFT = "l"
RIGHT = "r"
SLIGHT_LEFT = "L"
SLIGHT_RIGHT = "R"

class StrSumo:
    def __init__(self, route_controller, connection_info, controlled_vehicles):
        """
        :param route_controller: object that implements the scheduling algorithm for controlled vehicles
        :param connection_info: object that includes the map information
        :param controlled_vehicles: a dictionary that includes the vehicles under control
        """
        self.direction_choices = [STRAIGHT, TURN_AROUND, SLIGHT_RIGHT, RIGHT, SLIGHT_LEFT, LEFT]
        self.connection_info = connection_info
        self.route_controller = route_controller
        self.controlled_vehicles =  controlled_vehicles # dictionary of Vehicles by id
        #print(self.controlled_vehicles)

    def run(self):
        """
        Runs the SUMO simulation
        At each time-step, cars that have moved edges make a decision based on user-supplied scheduler algorithm
        Decisions are enforced in SUMO by setting the destination of the vehicle to the result of the
        :returns: total time, number of cars that reached their destination, number of deadlines missed
        """
        total_time = 0
        end_number = 0
        deadlines_missed = []

        step = 0
        vehicles_to_direct = [] #  the batch of controlled vehicles passed to make_decisions()
        vehicle_IDs_in_simulation = []

        try:
            while traci.simulation.getMinExpectedNumber() > 0:
                vehicle_ids = set(traci.vehicle.getIDList())

                # store edge vehicle counts in connection_info.edge_vehicle_count
                self.get_edge_vehicle_counts()
                #initialize vehicles to be directed
                vehicles_to_direct = []
                # iterate through vehicles currently in simulation
                for vehicle_id in vehicle_ids:

                    #should not be added because there is no corresponding -1, this makes edge_vehicle_count becomes the total number of vehicles that used to be on this edge.
                    #self.connection_info.edge_vehicle_count[traci.vehicle.getRoadID(vehicle_id)] += 1
                    
                    

                    # handle newly arrived controlled vehicles
                    if vehicle_id not in vehicle_IDs_in_simulation and vehicle_id in self.controlled_vehicles:
                        vehicle_IDs_in_simulation.append(vehicle_id)
                        traci.vehicle.setColor(vehicle_id, (255, 0, 0)) # set color so we can visually track controlled vehicles
                        self.controlled_vehicles[vehicle_id].start_time = float(step)#Use the detected release time as start time

                    if vehicle_id in self.controlled_vehicles.keys():
                        current_edge = traci.vehicle.getRoadID(vehicle_id)

                        if current_edge not in self.connection_info.edge_index_dict.keys():
                            continue
                        elif current_edge == self.controlled_vehicles[vehicle_id].destination:
                            continue

                        #print("{} now on: {}, records on {}; {} ".format(vehicle_id, current_edge, self.controlled_vehicles[vehicle_id].current_edge, current_edge!=self.controlled_vehicles[vehicle_id].current_edge))
                        if current_edge != self.controlled_vehicles[vehicle_id].current_edge:
                            self.controlled_vehicles[vehicle_id].current_edge = current_edge
                            self.controlled_vehicles[vehicle_id].current_speed = traci.vehicle.getSpeed(vehicle_id)
                            vehicles_to_direct.append(self.controlled_vehicles[vehicle_id])
                #print(len(vehicles_to_direct))
                vehicle_decisions_by_id = self.route_controller.make_decisions(vehicles_to_direct, self.connection_info)
                for vehicle_id, local_target_edge in vehicle_decisions_by_id.items():
                    # if decision not in self.connection_info.outgoing_edges_dict[self.controlled_vehicles[vehicle_id].current_edge]:
                    #     raise ValueError(f'{decision} does not lead to a valid edge from edge '
                    #                      f'{self.controlled_vehicles[vehicle_id].current_edge}')
                    #
                    # current_edge_of_vehicle = self.controlled_vehicles[vehicle_id].current_edge
                    # target_edge = self.connection_info.outgoing_edges_dict[current_edge_of_vehicle][decision]
                    if vehicle_id in traci.vehicle.getIDList():
                        #print("Changing the target of {} to {} with length {}".format(vehicle_id, local_target_edge, self.connection_info.edge_length_dict[local_target_edge]))
                        traci.vehicle.changeTarget(vehicle_id, local_target_edge)
                        self.controlled_vehicles[vehicle_id].local_destination = local_target_edge

                arrived_at_destination = traci.simulation.getArrivedIDList()

                for vehicle_id in arrived_at_destination:
                    if vehicle_id in self.controlled_vehicles:
                        #print the raw result out to the terminal
                        arrived_at_destination = False
                        if self.controlled_vehicles[vehicle_id].local_destination == self.controlled_vehicles[vehicle_id].destination:
                            arrived_at_destination = True
                        time_span = step - self.controlled_vehicles[vehicle_id].start_time
                        total_time += time_span
                        miss = False
                        if step > self.controlled_vehicles[vehicle_id].deadline:
                            deadlines_missed.append(vehicle_id)
                            miss = True
                        end_number += 1
                        print("Vehicle {} reaches the destination: {}, timespan: {}, deadline missed: {}"\
                            .format(vehicle_id, arrived_at_destination, time_span, miss))
                        #if not arrived_at_destination:
                            #print("{} - {}".format(self.controlled_vehicles[vehicle_id].local_destination, self.controlled_vehicles[vehicle_id].destination))

                traci.simulationStep()
                step += 1

                if step > MAX_SIMULATION_STEPS:
                    print('Ending due to timeout.')
                    break

        except ValueError as err:
            print('Exception caught.')
            print(err)

        num_deadlines_missed = len(deadlines_missed)

        return total_time, end_number, num_deadlines_missed

    def get_edge_vehicle_counts(self):
        for edge in self.connection_info.edge_list:
            self.connection_info.edge_vehicle_count[edge] = traci.edge.getLastStepVehicleNumber(edge)

