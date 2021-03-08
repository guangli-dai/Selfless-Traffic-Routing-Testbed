import os
import sys
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("No environment variable SUMO_HOME!")
from sumolib import net
import sumolib

class Vehicle:
    def __init__(self, vehicle_id, destination, start_time, deadline):
        """
        Args:
                vehicle_id:         type: string. The id of the vehicle.
                destination:        type: string. The id of the edge where the vehicle targets.
                start_time:         type: float. The step # when the vehicle is released. This value will be updated by STR_SUMO.
                deadline:           type: float. The deadline for this vehicle to reach the end of the target edge.
        """
        self.vehicle_id = vehicle_id
        self.destination = destination
        self.start_time = start_time
        self.deadline = deadline
        self.current_edge = ""
        self.current_speed = 0.0
        self.local_destination = ""


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
        self.net_filename = net_file
        net = sumolib.net.readNet(net_file)
        self.outgoing_edges_dict = {}
        self.edge_length_dict = {}
        self.edge_index_dict = {}
        self.edge_vehicle_count = {}
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
                print(current_edge_id + "already exists!")
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
                    self.outgoing_edges_dict[current_edge_id][direction] = current_outgoing_edge.getID()
