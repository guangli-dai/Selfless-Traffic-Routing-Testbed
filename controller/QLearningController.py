from controller.RouteController import RouteController
from core.Util import ConnectionInfo, Vehicle
from keras.models import load_model
import numpy as np
import traci


class QLearningPolicy(RouteController):
    def __init__(self, connection_info, model_file):
        super().__init__(connection_info)
        self.model = load_model(model_file)

    def make_decisions(self, vehicles, connection_info: ConnectionInfo):
        local_targets = {}

        for vehicle in vehicles:

            wrong_decision = False
            total_length = 0.0
            start_edge = vehicle.current_edge
            decision_list = []

            if vehicle.destination == vehicle.current_edge:
                continue

            #i = 0

            while total_length < connection_info.edge_length_dict[vehicle.current_edge]:
                state = self.getState(start_edge)
                action = self.act(state)
                action = self.direction_choices[action]
                if action not in connection_info.outgoing_edges_dict[start_edge]:
                    print("Impossible turns made for vehicle #" + str(vehicle.vehicle_id) + " : " + action + " @ " + str(start_edge))
                    wrong_decision = True
                    break

                print("Choice for " + str(start_edge) + " is: " + action)

                target_edge = connection_info.outgoing_edges_dict[start_edge][action]
                start_edge = target_edge
                decision_list.append(action)
                total_length += self.connection_info.edge_length_dict[target_edge]
                #
                #
                # if i > 0:
                #     if decision_list[i - 1] == decision_list[i] and decision_list[i] == 't':
                #         # stuck in a turnaround loop, let TRACI remove vehicle
                #         break

                #i += 1

            if wrong_decision:
                continue

            local_targets[vehicle.vehicle_id] = self.compute_local_target(decision_list, vehicle)

        return local_targets



    # this function reacheds the Neural Network trained before and let it make a decision for the situation now
    def act(self, state):
        act_values = self.model.predict(state)
        state_vals = state[0][1:7]
        state_vals = state_vals.reshape(act_values.shape)
        #print(state)
        mod_values = act_values - 10000 * (1 - state_vals)
        #print(mod_values)
        #print('**************************')
        return np.argmax(mod_values[0])

    # this function gives the current state of the vehicle based on the state size
    def getState(self, edge_now):
        en = edge_now
        state = []
        state.append(self.connection_info.edge_index_dict[en])
        for c in self.direction_choices:
            if c in self.connection_info.outgoing_edges_dict[en].keys():
                state.append(1)
                # 1 stands for the edge is available for being chose
            else:
                state.append(0)
                # 0 means this action cannot be chosen.
        # put the congestion ratio of all edges into the state.
        for edge_now in self.connection_info.edge_list:
            car_num = traci.edge.getLastStepVehicleNumber(edge_now)
            density = car_num / self.connection_info.edge_length_dict[edge_now]
            state.append(density)

        state = np.reshape(state, [1, len(state)])
        return state
