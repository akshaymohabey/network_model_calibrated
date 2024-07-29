"""
Akshay Mohabey
Python 3.12.4 
Mac OSX
19 July 2024

Network Model Calibrated
Agents File
"""

# Importing Dependencies
import mesa
import parameters as p
import random
import functions as f
import copy


# Agent Class

class People(mesa.Agent):
    def __init__(self,unique_ID, model,sts):

        # Initialize Parent Class
        super().__init__(unique_ID,model)
        self.ID = unique_ID
        self.state = random.choice(range(sts))
        self.incoming_connections = []
        self.outgoing_connections = []
        # Print Agent ID & State
        # print(f'Agent{self.ID} | State {self.state}')

    # @property
    def return_ID(self):
        return self.ID
    
    # @property
    def return_state(self):
        return self.state
    
    # Connection setter
    def set_connections(self,connection_list):
        self.incoming_connections = copy.copy(connection_list)
        self.outgoing_connections = copy.copy(connection_list)
    
    # Returns State List
    def return_connection_states_list(self):
        states_list = []
        for agent in self.incoming_connections:
            states_list.append(agent.state)
        return states_list

    # Modifying States
    def modify_state(self,state_list):
        most_common = f.most_common_list(state_list)
        self.state = random.choice(most_common)
    
    # # Should this come here
    # def return_connections(self):
    #     return self.incoming_connections

    def step(self):
        # Print Neighbors list
        # print(f'Agent: {self.ID} | State: {self.state}')
        states_list = self.return_connection_states_list()
        self.modify_state(states_list)



    
