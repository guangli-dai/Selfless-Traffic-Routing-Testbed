import os
import sys
import optparse
import xml.dom.minidom

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
NET_FILENAME = "test.net.xml"

STRAIGHT = "s"
TURN_AROUND = "t"
LEFT = "l"
RIGHT = "r"
SLIGHT_LEFT = "L"
SLIGHT_RIGHT = "R"

class StrSumo:
    def __init__(self, route_controller):
        """
        :param route_controller: object that implements the scheduling algorithm for controlled vehicles
        """
        self.direction_choices = [STRAIGHT, TURN_AROUND, SLIGHT_RIGHT, RIGHT, SLIGHT_LEFT, LEFT]
        self.connection_info = ConnectionInfo(NET_FILENAME)
        self.route_controller = route_controller(self.connection_info)
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
        #previous_edge = {}
        #current_edge = {}
        #entry_time_step = {}  # tracks the time step of each vehicle's entry to the simulation

        while traci.simulation.getMinExpectedNumber() > 0:
            # make a decision for each vehicle
            vehicle_ids = set(traci.vehicle.getIDList())

            # TODO - there is probably a more efficient way to calculate cars per edge
            self.connection_info.edge_vehicle_count.clear()

            # iterate through vehicles currently in simulation
            for vehicle_id in vehicle_ids:

                # TODO - there is probably a more efficient way to calculate cars per edge
                self.connection_info.edge_vehicle_count[traci.vehicle.getRoadID(vehicle_id)] += 1

                # handle newly arrived controlled vehicles
                if vehicle_id not in entry_time_step.keys() and vehicle_id in self.controlled_vehicles:
                    #entry_time_step[vehicle_id] = step #  now stored in Vehicle object set at init
                    #previous_edge[vehicle_id] = "" #  now stored in Vehicle object and set at init
                    #current_edge[vehicle_id] = traci.vehicle.getRoadID(vehicle_id) #  now stored in Vehicle object and set at init

                    traci.vehicle.setColor(vehicle_id, (255, 0, 0))

                if vehicle_id in self.controlled_vehicles:
                    current_edge = traci.vehicle.getRoadID(vehicle_id)

                    if current_edge not in self.connection_info.edge_index_dict.keys():
                        continue  # road is not valid(?)
                    elif current_edge == destination[vehicle_id]:
                        continue

                    if current_edge != self.controlled_vehicles[vehicle_id].current_edge:
                        self.controlled_vehicles[vehicle_id].current_edge = current_edge
                        vehicles_to_direct.append(self.controlled_vehicles[vehicle_id])

            vehicle_decisions_by_id = self.route_controller.make_decisions(vehicles_to_direct, self.connection_info)

            for vehicle_id, decision in vehicle_decisions_by_id:
                #  find the edge pointed to by the direction found in make_decision
                current_edge_of_vehicle = self.controlled_vehicles[vehicle_id].current_edge
                target_edge = self.connection_info.outgoing_edges_dict[current_edge_edge_of_vehicle][decision]
                traci.vehicle.changeTarget(vehicle_id, target_edge)

            arrived_at_destination = traci.simulation.getArrivedIDList() #  TODO: not sure this is the right way to get finished vehicles, since we change TRACI targets to direct vehicles

            for vehicle_id in arrived_at_destination:
                if vehicle_id in self.controlled_vehicles:
                    total_time += step - entry_time_step[vehicle_id]
                    end_number += 1
                    if step > self.controlled_vehicles[vehicle_id].deadline:
                        deadlines_missed.append(vehicle_id)

                del entry_time_step[vehicle_id]

            traci.simulationStep()
            step += 1

            if step >= MAX_SIMULATION_STEPS:
                break


        return total_time, end_number, deadlines_missed

    #  This is a dummy method for getting vehicles; the vehicle generation code will provide the list of controlled vehicles in practice
    def get_controlled_vehicles(self):
        vehicle_list = {}

        #  just generate 1000 dummy vehicles for now...
        for i in range(1000):
            new_vehicle = Vehicle(i, "", 0, float('inf'))
            vehicle_list[i] = new_vehicle

        return vehicle_list

class Vehicle:
    def __init__(self, vehicle_id, destination, start_time, deadline):
        self.vehicle_id = vehicle_id
        self.destination = destination
        self.start_time = start_time
        self.deadline = deadline
        self.current_edge = ""


class ConnectionInfo:
    """
    Parses and stores network information from net_file  as collections.
    The idea is to use this information in the scheduling algorithm.
    Available collections:
        - out_going_edges_dict {edge_id: {direction: out_edge}}
        - edge_length_dict {edge_id: edge_length}
        - edge_index_dict {edge_index_dict} keep track of edge ids by an index
        - edge_vehicle_count {edge_id: number of vehicles at edge}
        - edge_list [edge_id]
    :param net_file: file name of a SUMO network file, e.g. 'test.net.xml'
    """
    def __init__(self, net_file):
        net = sumolib.net.readNet(net_file)
        self.outgoing_edges_dict = {}
        self.edge_length_dict = {}
        self.edge_index_dict = {}  #
        self.edge_vehicle_count = {} #
        self.edge_list = []

        edge_index = 0

        edges = net.getEdges()

        # collect edge information into dictionaries
        for current_edge in edges:
            current_edge_id = current_edge.getID()

            # add edge to edge list if it allows passenger vehicles
            # "passenger" is a SUMO defined vehicle class
            if current_edge.allows("passenger"):
                self.edge_list.append(current_edge_id)

            if current_edge_id in self.edge_index_dict.keys():
                print(current_edge_id + "already exists!")
            else:
                self.edge_index_dict[current_edge_id] = edge_index
                edge_index += 1
            if current_edge_id in self.outgoing_edges_dict.keys():
                print(current_edge_id + "already exists!")
            else:
                self.outgoing_edges_dict[current_edge_id] = {}
            if current_edge_id in self.edge_length_dict.keys():
                print(edge_now_id + "already exists!")
            else:
                self.edge_length_dict[current_edge_id] = current_edge.getLength()

            # collect outgoing edges by direction
            outgoing_edges = current_edge.getOutgoing()
            for current_outgoing_edge in outgoing_edges:
                if not current_outgoing_edge.allows("passenger"):
                    continue
                connections = current_edge.getConnections(current_outgoing_edge)
                for connection in connections:
                    direction = connection.getDirection()
                    self.outgoing_edges_dict[current_edge_id][direction] = current_outgoing_edge.getId()
