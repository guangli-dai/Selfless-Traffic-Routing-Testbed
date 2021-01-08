***Description of the project***

**Target (What is this project about?)**

* Builds a test bed for selfless traffic routing based on SUMO: STR-SUMO.
* Tests existing selfish traffic routing algorithms on STR-SUMO.
* Develops and tests heuristic selfless traffic routing algorithms on STR-SUMO.

**Usage (How to use the project)**
To run the project, you need at least two self-defined components:
* A map in the form of XML. Some sample maps are given in the test directory. More sample maps will be given.
* A route controller inheriting class RouteController that includes a self-defined function make_decisions.

With the two components ready, you can start testing the routing policy using the codes below (extracted from test/test_main_STR_SUMO.py). Specifically, the codes below uses the DijkstraPolicy.

```
from STR_SUMO import StrSumo
import os
import sys
from xml.dom.minidom import parse, parseString
from Util import *
from RouteController import *
from DijkstraController import DijkstraPolicy

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("No environment variable SUMO_HOME!")

from sumolib import checkBinary
import traci

def run_simulation(scheduler):
    simulation = StrSumo(scheduler, init_connection_info, route_file)

    traci.start([sumo_binary, "-c", "myconfig.sumocfg",
                 "--tripinfo-output", "trips.trips.xml", "--fcd-output", "testTrace.xml"])

    total_time, end_number, deadlines_missed = simulation.run()
    print(str(total_time) + ' for ' + str(end_number) + ' vehicles.')
    print(str(deadlines_missed) + ' deadlines missed.')

sumo_binary = checkBinary('sumo-gui')#test with gui
# sumo_binary = checkBinary('sumo')#test without gui

# parse config file for map file name
dom = parse("myconfig.sumocfg")

net_file_node = dom.getElementsByTagName('net-file')
net_file_attr = net_file_node[0].attributes

net_file = net_file_attr['value'].nodeValue
init_connection_info = ConnectionInfo(net_file)

route_file_node = dom.getElementsByTagName('route-files')
route_file_attr = route_file_node[0].attributes
route_file = route_file_attr['value'].nodeValue

print("Testing Dijkstra's Algorithm Route Controller")
scheduler = DijkstraPolicy(init_connection_info)
run_simulation(scheduler)
```

***Contribution Guidance***

**Codes**
Please add comments for each function using the style pydoc can recognize: https://stackoverflow.com/questions/13040646/how-do-i-create-documentation-with-pydoc

You are also recommended to add brief comments to state the function of each block of codes. Naming variables using convention lowercae_with_underscores is suggested.

**Tests**
For important functions, please write a simple test case naming as test_function_name.py. After the test is passed, archive it in the test directory. When reviewing codes, this would be helpful for code reviewers to understand the usage of functions and to expand the tests with some border cases.
