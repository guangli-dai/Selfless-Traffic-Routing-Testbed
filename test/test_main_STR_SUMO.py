'''
This test file needs the following files:
STR_SUMO.py, RouteController.py, Util.py, test.net.xml, test.rou.xml, myconfig.sumocfg and corresponding SUMO libraries.
'''
from core.STR_SUMO import StrSumo
import os
import sys
from xml.dom.minidom import parse, parseString
from core.Util import *
from controller.RouteController import *
from controller.DijkstraController import DijkstraPolicy
from QLearningController import QLearningPolicy

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("No environment variable SUMO_HOME!")

from sumolib import checkBinary
import traci

sumo_binary = checkBinary('sumo-gui')
# sumo_binary = checkBinary('sumo')

# parse config file for map file name
dom = parse("./configurations/myconfig.sumocfg")

net_file_node = dom.getElementsByTagName('net-file')
net_file_attr = net_file_node[0].attributes

net_file = net_file_attr['value'].nodeValue
init_connection_info = ConnectionInfo("./configurations/"+net_file)

route_file_node = dom.getElementsByTagName('route-files')
route_file_attr = route_file_node[0].attributes
route_file = route_file_attr['value'].nodeValue


def test_random_policy():
    scheduler = RandomPolicy(init_connection_info)
    run_simulation(scheduler)


def test_q_learning():
    print("Testing Q Learning Route Controller")
    scheduler = QLearningPolicy(init_connection_info, './rl-high-all-fixed-late.h5')
    run_simulation(scheduler)
    print("TEST PASSED!")
    print("************")


def test_dijkstra_policy():
    print("Testing Dijkstra's Algorithm Route Controller")
    scheduler = DijkstraPolicy(init_connection_info)
    run_simulation(scheduler)
    print("TEST PASSED")
    print("***********")


def run_simulation(scheduler):
    simulation = StrSumo(scheduler, init_connection_info, route_file)

    traci.start([sumo_binary, "-c", "./configurations/myconfig.sumocfg",
                 "--tripinfo-output", "./configurations/trips.trips.xml", "--fcd-output", "./configurations/testTrace.xml"])

    total_time, end_number, deadlines_missed = simulation.run()
    print(str(total_time) + ' for ' + str(end_number) + ' vehicles.')
    print(str(deadlines_missed) + ' deadlines missed.')


test_dijkstra_policy()
