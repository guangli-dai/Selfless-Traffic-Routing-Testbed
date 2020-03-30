'''
This test file needs the following files:
STR_SUMO.py, RouteController.py, Util.py, test.net.xml, test.rou.xml, myconfig.sumocfg and corresponding SUMO libraries.
'''
from STR_SUMO import StrSumo
import os
import sys
from xml.dom.minidom import parse, parseString
from Util import *
from RouteController import *
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("No environment variable SUMO_HOME!")

from sumolib import checkBinary
import traci

#sumo_binary = checkBinary('sumo-gui')
sumo_binary = checkBinary('sumo')

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


total_time, end_number, deadlines_missed = simulation.run()
print(str(total_time) + ' for ' + str(end_number) + ' vehicles.')
print(str(deadlines_missed) +' deadlines missed.')