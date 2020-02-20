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
        :param route_controller: uses a scheduling algorithm to make vehicle routing decisions
        """
        self.direction_choices = [STRAIGHT, TURN_AROUND, SLIGHT_RIGHT, RIGHT, SLIGHT_LEFT, LEFT]
        self.connection_info = ConnectionInfo(NET_FILENAME)
        self.route_controller = route_controller(self.connection_info)
        self.controlled_vehicles = self.get_controlled_vehicles()

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
        previous_edge = {}
        current_edge = {}
        entry_time_step = {}  # tracks the time step of each vehicle's entry to the simulation

        while traci.simulation.getMinExpectedNumber() > 0:
            # make a decision for each vehicle
            vehicle_ids = set(traci.vehicle.getIDList())

            # iterate through vehicles currently in simulation
            for vehicle_id in vehicle_ids:

                # handle newly arrived controlled vehicles
                if vehicle_id not in entry_time_step.keys() and vehicle_id in self.controlled_vehicles:
                    entry_time_step[vehicle_id] = step
                    previous_edge[vehicle_id] = ""
                    current_edge[vehicle_id] = traci.vehicle.getRoadID(vehicle_id)

                    traci.vehicle.setColor(vehicle_id, (255, 0, 0))

                if vehicle_id in self.controlled_vehicles:
                    temp_curr_edge = traci.vehicle.getRoadID(vehicle_id)

                    if temp_curr_edge not in self.connection_info.edge_index_dict.keys():
                        continue  # road is not valid(?)
                    elif temp_curr_edge == destination[vehicle_id]: # QUESTION: how are we keeping track of destinations?
                        continue

                    current_edge[vehicle_id] = temp_curr_edge
                    if current_edge[vehicle_id] != previous_edge[vehicle_id]:
                        # make a decision and set traci target to that decision
                        action = self.route_controller.make_decision(vehicle_id)

                        # TODO: error check action

                        target_edge = self.connection_info.outgoing_edges_dict[vehicle_id][action]
                        previous_edge[vehicle_id] = current_edge
                        traci.vehicle.changeTarget(vehicle_id, target_edge)


            arrived_at_destination = traci.simulation.getArrivedIDList()

            for vehicle_id in arrived_at_destination:
                if vehicle_id in self.controlled_vehicles:
                    total_time += step - entry_time_step[vehicle_id]
                    end_number += 1
                del entry_time_step[vehicle_id]

            traci.simulationStep()
            step += 1

            if step >= MAX_SIMULATION_STEPS:
                break


        return total_time, end_number, deadlines_missed

    def get_controlled_vehicles(self):
        return []


class ConnectionInfo(self):
    """
    Parses and stores network information from net_file to be used by scheduler algorithms
    :param net_file: file name of a SUMO network file, e.g. 'test.net.xml'
    """
    def __init__(self, net_file):
        net = sumolib.net.readNet(net_file)
        self.outgoing_edges_dict = {}  # {edge_id: {direction: out_edge}}
        self.edge_length_dict = {}  # {edge_id: edge_length}
        self.edge_index_dict = {}  # {edge_index_dict} keep track of edge ids by an index
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


# dummy_algo = algorithm()
# simulation = STR_SUMO()
# simulation.run()
