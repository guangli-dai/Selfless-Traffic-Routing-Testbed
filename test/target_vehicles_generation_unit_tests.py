"""
    File for unit-testing the function
        @target_vehicles_generator.generate_target_vehicles
    from the file "target_vehicles_generation_protocols.py".
"""
import random
import network_map_data_structures
import target_vehicles_generation_protocols as TVGProt




def print_test_passed():
    print("---> TEST PASSED")
    
def print_test_failed():
    print("---> TEST FAILED")



# Create generator and read in data of traffic network:
generator = TVGProt.target_vehicles_generator()
generator.net = network_map_data_structures.getNetInfo("test.net.xml")
[generator.length_dict, generator.out_dict, generator.index_dict, generator.edge_list] = network_map_data_structures.getEdgesInfo(generator.net)



# Start unit-testing:
print("************** generate_with_one_start_one_dest ******************\n")
param_start = random.choice(generator.edge_list)
param_dest = random.choice(generator.edge_list)
result_dict = generator.generate_target_vehicles(5, "test.rou.xml", (param_start, param_dest) )
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


print("************** generate_with_ranged_starts_one_dest ******************\n")
param_start = TVGProt.__random_choices_with_rp__(generator.edge_list, 30)
param_dest = random.choice(generator.edge_list)
result_dict = generator.generate_target_vehicles(5, "test.rou.xml", (param_start, param_dest) )
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


print("************** generate_with_ranged_starts_ranged_dests ******************\n")
param_start = TVGProt.__random_choices_with_rp__(generator.edge_list, 30)
param_dest = TVGProt.__random_choices_with_rp__(generator.edge_list, 30)
result_dict = generator.generate_target_vehicles(5, "test.rou.xml", (param_start, param_dest) )
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
result_dict = generator.generate_target_vehicles(5, "test.rou.xml")
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
result_dict = generator.generate_target_vehicles(5, "test.rou.xml", param_pattern)
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
result_dict = generator.generate_target_vehicles(5, "test.rou.xml", (param_start, param_dest) )
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
result_dict = generator.generate_target_vehicles(5, "test.rou.xml", (param_start, param_dest) )
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
result_dict = generator.generate_target_vehicles(5, "test.rou.xml", (param_start, param_dest) )
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
