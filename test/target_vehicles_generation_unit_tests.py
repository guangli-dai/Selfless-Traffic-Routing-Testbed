"""
    File for unit-testing the function
        @target_vehicles_generator.generate_target_vehicles
    from the file "target_vehicles_generation_protocols.py".
    File needed for the test: test.net.xml
    File that will be generated during the unit test includes test.pattern1*.xml, test.pattern2*.xml, test.pattern3*.xml
"""
import random
from core import network_map_data_structures
import core.target_vehicles_generation_protocols as TVGProt




def print_test_passed():
    print("---> TEST PASSED")
    
def print_test_failed():
    print("---> TEST FAILED")
#TODO: add invokes of remove_temp_files
def remove_temp_files(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)


# Create generator and read in data of traffic network:
generator = TVGProt.target_vehicles_generator()
generator.net = network_map_data_structures.getNetInfo("./configurations/test.net.xml")
[generator.length_dict, generator.out_dict, generator.index_dict, generator.edge_list] = network_map_data_structures.getEdgesInfo(generator.net)



# Start unit-testing:
print("************** generate_with_one_start_one_dest ******************\n")
param_start = random.choice(generator.edge_list)
param_dest = random.choice(generator.edge_list)
result_dict = generator.generate_target_vehicles(5, "./configurations/test.rou.xml", (param_start, param_dest) )
error_message = result_dict[TVGProt.target_vehicles_generator.__ERROR_MESSAGE__]
result_lst = result_dict[TVGProt.target_vehicles_generator.VEHICLES_INFO]
if error_message == None:
    if result_lst != None:
        for result in result_lst:
            print(result[0], result[1][0].getID(), result[1][1].getID(), result[2])
    print_test_passed()
else:
    print(error_message)
    print_test_failed()
print("\n")

#this unit test may cause indefinite loop or even dead loop if the start points and the destination are not connected!
print("************** generate_with_ranged_starts_one_dest ******************\n")
param_start = TVGProt.__random_choices_with_rp__(generator.edge_list, 30)
param_dest = random.choice(generator.edge_list)
result_dict = generator.generate_target_vehicles(5, "./configurations/test.rou.xml", (param_start, param_dest) )
error_message = result_dict[TVGProt.target_vehicles_generator.__ERROR_MESSAGE__]
result_lst = result_dict[TVGProt.target_vehicles_generator.VEHICLES_INFO]
if error_message == None:
    for result in result_lst:
        print(result[0], result[1][0].getID(), result[1][1].getID(), result[2])
    print_test_passed()
else:
    print(error_message)
    print_test_failed()
print("\n")

#this unit test may cause indefinite loop or even dead loop if all pairs of start point and the destination are not connected!
print("************** generate_with_ranged_starts_ranged_dests ******************\n")
param_start = TVGProt.__random_choices_with_rp__(generator.edge_list, 30)
param_dest = TVGProt.__random_choices_with_rp__(generator.edge_list, 30)
result_dict = generator.generate_target_vehicles(5, "./configurations/test.rou.xml", (param_start, param_dest) )
error_message = result_dict[TVGProt.target_vehicles_generator.__ERROR_MESSAGE__]
result_lst = result_dict[TVGProt.target_vehicles_generator.VEHICLES_INFO]
if error_message == None:
    for result in result_lst:
        print(result[0], result[1][0].getID(), result[1][1].getID(), result[2])
    print_test_passed()
else:
    print(error_message)
    print_test_failed()
print("\n")


print("************** generate_with_rand_starts_rand_dests ******************\n")
result_dict = generator.generate_target_vehicles(5, "./configurations/test.rou.xml")
error_message = result_dict[TVGProt.target_vehicles_generator.__ERROR_MESSAGE__]
result_lst = result_dict[TVGProt.target_vehicles_generator.VEHICLES_INFO]
if error_message == None:
    for result in result_lst:
        print(result[0], result[1][0].getID(), result[1][1].getID(), result[2])
    print_test_passed()
else:
    print(error_message)
    print_test_failed()
print("\n")


print("************** generate with non-tuple and non-None pattern  ******************\n")
param_pattern = "Invalid"
result_dict = generator.generate_target_vehicles(5, "./configurations/test.rou.xml", param_pattern)
error_message = result_dict[TVGProt.target_vehicles_generator.__ERROR_MESSAGE__]
result_lst = result_dict[TVGProt.target_vehicles_generator.VEHICLES_INFO]
if error_message == None:
    if result_lst != None:
        for result in result_lst:
            print(result[0], result[1][0].getID(), result[1][1].getID(), result[2])
    print_test_failed()
else:
    print(error_message)
    if result_lst == None:
        # This means that the function
        # target_vehicles_generator.generate_with_one_start_one_dest was executed,
        # which is not desired.
        print_test_failed()
    elif len(result_lst) == 0:
        print_test_passed()
    else:
        # No vehicle ID should be produced.
        print_test_failed()
print("\n")


print("************** generate with invalid tuple elements ******************\n")
param_start = "Invalid"
param_dest = "Invalid"
result_dict = generator.generate_target_vehicles(5, "./configurations/test.rou.xml", (param_start, param_dest) )
error_message = result_dict[TVGProt.target_vehicles_generator.__ERROR_MESSAGE__]
result_lst = result_dict[TVGProt.target_vehicles_generator.VEHICLES_INFO]
if error_message == None:
    for result in result_lst:
        print(result[0], result[1][0].getID(), result[1][1].getID(), result[2])
    print_test_failed()
else:
    print(error_message)
    if len(result_lst) == 0:
        print_test_passed()
    else:
        # No vehicle ID should be produced.
        print_test_failed()
print("\n")


print("************** generate with invalid 0th tuple element ******************\n")
param_start = "Invalid"
param_dest = random.choice(generator.edge_list)
result_dict = generator.generate_target_vehicles(5, "./configurations/test.rou.xml", (param_start, param_dest) )
error_message = result_dict[TVGProt.target_vehicles_generator.__ERROR_MESSAGE__]
result_lst = result_dict[TVGProt.target_vehicles_generator.VEHICLES_INFO]
if error_message == None:
    for result in result_lst:
        print(result[0], result[1][0].getID(), result[1][1].getID(), result[2])
    print_test_failed()
else:
    print(error_message)
    if len(result_lst) == 0:
        print_test_passed()
    else:
        # No vehicle ID should be produced.
        print_test_failed()
print("\n")


print("************** generate with invalid 1st tuple element ******************\n")
param_start = TVGProt.__random_choices_with_rp__(generator.edge_list, 10)
param_dest = "Invalid"
result_dict = generator.generate_target_vehicles(5, "./configurations/test.rou.xml", (param_start, param_dest) )
error_message = result_dict[TVGProt.target_vehicles_generator.__ERROR_MESSAGE__]
result_lst = result_dict[TVGProt.target_vehicles_generator.VEHICLES_INFO]
if error_message == None:
    for result in result_lst:
        print(result[0], result[1][0].getID(), result[1][1].getID(), result[2])
    print_test_failed()
else:
    print(error_message)
    if len(result_lst) == 0:
        print_test_passed()
    else:
        # No vehicle ID should be produced.
        print_test_failed()
print("\n")


print("************** generate random vehicles' xml file one start one end point ******************\n")
vehicle_list = generator.generate_vehicles(10, 100, 1, "test.pattern1.xml", "./configurations/test.net.xml")
if vehicle_list is not None:
    for v in vehicle_list:
        print(str(v.vehicle_id) + ':'+v.destination+' from '+str(v.start_time)+' to '+str(v.deadline))
    print_test_passed()
else:
    print_test_failed()
print ("\n")

print("************** generate random vehicles' xml file ranged start one end point ******************\n")
vehicle_list = generator.generate_vehicles(10, 100, 2, "test.pattern2.xml", "./configurations/test.net.xml")
if vehicle_list is not None:
    for v in vehicle_list:
        print(str(v.vehicle_id) + ':'+v.destination+' from '+str(v.start_time)+' to '+str(v.deadline))
    print_test_passed()
else:
    print_test_failed()
print ("\n")

print("************** generate random vehicles' xml file ranged start ranged end point ******************\n")
vehicle_list = generator.generate_vehicles(10, 100, 3, "test.pattern3.xml", "./configurations/test.net.xml")
if vehicle_list is not None:
    for v in vehicle_list:
        print(str(v.vehicle_id) + ':'+v.destination+' from '+str(v.start_time)+' to '+str(v.deadline))
    print_test_passed()
else:
    print_test_failed()
print ("\n")