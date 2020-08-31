from RouteController import RouteController
from Util import ConnectionInfo, Vehicle
import numpy as np
import traci
import math


class DijkstraPolicy(RouteController):
    complete = []
    test_22 = []
    count = 0

    def __init__(self, connection_info):
        super().__init__(connection_info)

    def make_decisions(self, vehicles, connection_info):
        """
        make_decisions algorithm uses Dijkstra's Algorithm to find the shortest path to each individual vehicle's destination
        :param vehicles: list of vehicles on the map
        :param connection_info: information about the map (roads, junctions, etc)
        """
        local_targets = {}
        for vehicle in vehicles:
            if vehicle in self.complete:
                continue # skip vehicle if Dijkstra's has already been performed on it

            decision_list = []
            unvisited = {edge: 1000000000 for edge in self.connection_info.edge_list} # map of unvisited edges
            visited = {} # map of visited edges
            current_edge = vehicle.current_edge

            current_distance = self.connection_info.edge_length_dict[current_edge]
            unvisited[current_edge] = current_distance
            path_lists = {edge: [] for edge in self.connection_info.edge_list} #stores shortest path to each edge using directions

            while True:
                if current_edge not in self.connection_info.outgoing_edges_dict.keys():
                    continue
                for direction, outgoing_edge in self.connection_info.outgoing_edges_dict[current_edge].items():
                    if outgoing_edge not in unvisited:
                        continue
                    edge_length = self.connection_info.edge_length_dict[outgoing_edge]
                    new_distance = current_distance + edge_length
                    if new_distance < unvisited[outgoing_edge]:
                        unvisited[outgoing_edge] = new_distance
                        current_path = path_lists[current_edge]
                        current_path.append(direction)
                        path_lists[outgoing_edge] = current_path

                visited[current_edge] = current_distance
                del unvisited[current_edge]
                if not unvisited:
                    break
                possible_edges = [edge for edge in unvisited.items() if edge[1]]
                current_edge, current_distance = sorted(possible_edges, key=lambda x: x[1])[0]

            for direction in path_lists[vehicle.destination]:
                decision_list.append(direction)

            self.complete.append(vehicle) #adds vehicle to list of finished vehicles

            local_targets[vehicle.vehicle_id] = self.compute_local_target(decision_list, vehicle)

        return local_targets
