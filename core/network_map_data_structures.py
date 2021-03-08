"""
    This file contains functions to organise traffic network data
    into data structures in Python.
"""

import sys
import os

# !!! Code borrowed from Guangli !!!
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("No environment variable SUMO_HOME!")

from sumolib import checkBinary
import sumolib



def getNetInfo(net_file_name):
    """
        param @net_file_name <str>: name of/path to the XML file from which the
                                    map network information is to be retrieved.
        
        Function to retrieve the network information stored in @net_file_name;
        returns a sumolib.Net object if @net_file_name is in the correct file
        format, and 'None' otherwise.
    """
    if net_file_name.endswith('.net.xml'):
        return sumolib.net.readNet(net_file_name)
    
    ### UNCOMMENT TO DEBUG ###
    #print("Invalid File Format: Input file name must end with the suffix '.net.xml'!")
    
    return None


def getEdgesInfo(net):
    """
        param @net <sumolib.Net>: variable that stores the map network information.
        
        Function to retrieve the data of the edges. The return value is a list of
        four elements, which are respectively
            [0] a Python dictionary of the lengths of the edges.
            [1] a Python dictionary of the outgoings of the edges.
            [2] a Python dictionary of the index assignment of the edges.
            [3] a list of the edges. An edge element is of type sumolib.net.Edge.
    """
    out_dict = {}
    length_dict = {}
    index_dict = {}
    edge_list = []
    counter = 0
    all_edges = net.getEdges()
    #all_connections = net.getConnections()
    for current_edge in all_edges:
        current_edge_id = current_edge.getID()
        if current_edge.allows("passenger"):
            edge_list.append(current_edge)
        if current_edge_id in index_dict.keys():
            print(current_edge_id+" already exists!")
        else:
            index_dict[current_edge_id] = counter
            counter += 1
        if current_edge_id in out_dict.keys():
            print(current_edge_id+" already exists!")
        else:
            out_dict[current_edge_id] = {}
        if current_edge_id in length_dict.keys():
            print(current_edge_id+" already exists!")
        else:
            length_dict[current_edge_id] = current_edge.getLength()
        #edge_now is sumolib.net.edge.Edge
        out_edges = current_edge.getOutgoing()
        for current_out_edge in out_edges:
            if not current_out_edge.allows("passenger"):
                #print("Found some roads prohibited")
                continue
            conns = current_edge.getConnections(current_out_edge)
            for conn in conns:
                dir_now = conn.getDirection()
                out_dict[current_edge_id][dir_now] = current_out_edge.getID()

    return [length_dict, out_dict, index_dict, edge_list]
