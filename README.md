***Selfless Traffic Routing testbed based on SUMO (STR-SUMO)***

This project is built based on SUMO (https://sumo.dlr.de/docs/index.html#introduction), which offers a traffic simulation platform.
The goal of STR-SUMO is to offer a testbed that can benchmark the performance of a routing policy under the following constraints:
- Some vehicles are controlled by the scheudling algorithm;
- Each controlled vehicle has three parameters: 1. start point (an edge), 2. destination (an edge), 3. time to set off, 4. deadline. When travelling from the start point to the destination from the time to set off, the time a vehicle reaches the destination should not exceed the deadline;
The goal of the routing policy, i.e., the metrics used, includes:
- How many vehicles have missed their deadlines -- the smaller the better;
- What is the average time spent for all controlled vehicles -- the smaller the better.

***pre-requisite***

It is recommended to use Python 3.x, the packages required are included in requirements.txt. 
You can use pip to install them directly (for Python 3.x):
```
pip3 install requirements.txt
```
You also need to install SUMO properly: https://sumo.dlr.de/docs/Installing/index.html


***Layout of the repository***

main.py: The entrance of the project. Can simply run it when all pre-requisites are installed using:
```
python3 main.py
```
It will show the benchmarking results of the Dijkstra routing policy for a set of vehicles sharing the same start point and the same destination.

Next, we walk through each subdirectory.

**configurations**

Includes the mandatory configuration file: \*.sumocfg and \*.net.xml. Note that the \*.net.xml you specify in the sumocfg file must be placed directly in the configuration file repository.
More maps are given in “maps" subdirectory.

**core**

Includes the core files of STR-SUMO. 
- Util.py: includes the data structure used to store vehicle and map information;
- network_map_data_structure.py: includes the useful operations to get infromation of the current map;
- target_vehicles_generation_protocols.py: includes functions used to generate vehicles (including controlled vehicles' information and uncontrolled vehicles' routes)
- STR-SUMO.py: takes in a routing policy and performs the simulation to benchmark the performance of the target policy under a given set of map and vehicle sets.

**controller**

Includes different scheduling policies.
- RouteController.py: the base class of all routing policies;
- DijkstraController.py: the routing plicy that employs Dijkstra to find the shortest path (without considering the congestion) for each controlled vehicles;
- QLearningController.py: a simple routing policy using a trained agent. Specifically trained for map test.net.xml.

**test**

Includes the unit test for different core files.
The test scripts should be placed in the main repository.

***Contribution Guidance***

**Codes**

Please add comments for each function using the style pydoc can recognize: https://stackoverflow.com/questions/13040646/how-do-i-create-documentation-with-pydoc

You are also recommended to add brief comments to state the function of each block of codes. Naming variables using convention lowercae_with_underscores is suggested.

**Tests**

For important functions, please write a simple test case naming as test_function_name.py. After the test is passed, archive it in the test directory. When reviewing codes, this would be helpful for code reviewers to understand the usage of functions and to expand the tests with some border cases.
