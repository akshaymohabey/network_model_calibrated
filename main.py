"""
Akshay Mohabey
Python 3.12.4 
Mac OSX
19 July 2024

Network Model Calibrated
Model File
"""

# Import Dependencies
import mesa
import networkx as nx
import random
import parameters as p
import copy
import matplotlib.pyplot as plt
import agents
import functions as f


# Returns mos common state in the model
# Also add the proportion of the model in the model
def most_common_state(model):
    states = []
    for agent in model.grid.get_all_cell_contents():
        s = agent.return_state()
        states.append(s)
    c_state = random.choice(f.most_common_list(states))

    # Total States
    n = float(len(states))
    b = float(states.count(c_state))

    ratio = b/n
    # Print Most Common State
    # print(c_state)
    return ratio

#  Model Class
class NetworkModel(mesa.Model):
    def __init__(self,Sts):

        # Initializing Parent Class
        super().__init__()

        # All agent states
        # self.common_agents_state = 0

        # Generating Random Network
        # self.G = nx.erdos_renyi_graph(N,P)

        # Other Network Try
        # self.G = f.gnp_random_connected_graph(N,P)
        file_path = 'data/network.txt'
        # self.G = f.create_graph_from_file(file_path)
        self.G = f.generate_graph(file_path)



        # nx.write_gexf(self.G,"export/network_graph.gexf")

        # Initializing Network Grid
        self.grid = mesa.space.NetworkGrid(self.G)
        self.schedule = mesa.time.RandomActivation(self)
        self.running = True
        # print(nx.number_of_nodes(self.G))
        agent_no = 0
        

        # Adding agents to the model
        # Change this defination to include enumerate function
        for node in nx.nodes(self.G):
            a = agents.People(agent_no,self,Sts)
            self.schedule.add(a)
            self.grid.place_agent(a,node)
            agent_no += 1

        # Adding Connections to the agents
        for node in nx.nodes(self.G):
            a = []
            a.append(node)
            node_agents = self.grid.get_cell_list_contents(a)
            agent = node_agents[0]
            neighborhood_list = self.grid.get_neighborhood(node)
            neighbors = self.grid.get_cell_list_contents(neighborhood_list)
            agent.set_connections(neighbors)

         # Initiating Data Collector
        self.datacollector = mesa.DataCollector(
            model_reporters={"Most Common State": most_common_state}
            )
        
        # Drawing the Network Graph
        # nx.draw(self.G,
        #         with_labels = True,
        #         node_color = "green",
        #         node_size = 400,
        #         font_color = "white",
        #         font_family = "Times New Roman")
        # plt.margins(0.2)
        # plt.show()
    

    # Step/Game Function
    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()