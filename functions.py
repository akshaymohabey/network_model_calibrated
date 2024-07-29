"""
Akshay Mohabey
Python 3.12.4 
Mac OSX
19 July 2024

Network Model Calibrated
Functions File
"""
# Import Dependencies
import matplotlib.pyplot as plt
import networkx as nx
import parameters as p
import agents

from collections import Counter
from itertools import combinations, groupby
import random 

# Generating a random graph
"""
G = nx.generators.random_graphs.erdos_renyi_graph(p.num_of_agents,p.prob)
nx.draw(G)
plt.show()
"""

def most_common_list(states_list):
    if not states_list:
        return []
    
    count = Counter(states_list)
    max_count = max(count.values())
    most_common = [num for num, freq in count.items() if freq == max_count]
    return most_common

"""
Generates a random undirected graph, similarly to an Erdős-Rényi 
graph, but enforcing that the resulting graph is conneted
"""
def gnp_random_connected_graph(n, p):
   
    edges = combinations(range(n), 2)
    G = nx.Graph()
    G.add_nodes_from(range(n))
    if p <= 0:
        return G
    if p >= 1:
        return nx.complete_graph(n, create_using=G)
    for _, node_edges in groupby(edges, key=lambda x: x[0]):
        node_edges = list(node_edges)
        random_edge = random.choice(node_edges)
        G.add_edge(*random_edge)
        for e in node_edges:
            if random.random() < p:
                G.add_edge(*e)
    return G

"""
# Generates Graph from text file
"""
def create_graph_from_file(file_path):
    # Initialize the graph
    G = nx.Graph()

    # Read the file and cycle through each line
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Parse nodes and their connections
    for line in lines:
        if line.strip():  # Ignore empty lines
            parts = line.strip().split(',')
            node = int(parts[0])
            G.add_node(node)  # Add the node
            
            if len(parts) > 1:
                for neighbor in parts[1:]:
                    neighbor_node = int(neighbor)
                    G.add_edge(node, neighbor_node)
            else:
                # Node has no connections, will be handled after all nodes are added
                pass

    # Ensure nodes with no connections are connected to a random node
    all_nodes = list(G.nodes)
    print(len(all_nodes))
    for node in all_nodes:
        if len(list(G.neighbors(node))) == 0:  # Node has no neighbors
            random_node = random.choice(all_nodes)
            while random_node == node:  # Ensure not connecting to itself
                random_node = random.choice(all_nodes)
            G.add_edge(node,random_node)
    
    return G


# Running Tests on the gererated graph
"""
# Something wrong with the above exported graph
# Path to the file
file_path = 'data/network.txt'
graph = create_graph_from_file(file_path)

# Output some basic information about the graph
print(f"Graph has {graph.number_of_nodes()} nodes and {graph.number_of_edges()} edges.")

nx.write_gexf(graph,"export/network_graph.gexf")
# Something is wrong with the exported file
# Issue with Gephi
"""


def generate_graph(file_path):
    # Initialize a NetworkX graph
    G = nx.Graph()
    
    # Read the file content
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Dictionary to keep track of connections
    connections = {}
    
    # Parse the file to populate the connections dictionary
    for line in lines:
        parts = line.strip().split(',')
        node = int(parts[0])
        if len(parts) > 1:
            connected_nodes = [int(p) for p in parts[1:]]
        else:
            connected_nodes = []
        
        connections[node] = connected_nodes
    
    # Add nodes and edges to the graph
    for node, connected_nodes in connections.items():
        G.add_node(node)
        for connected_node in connected_nodes:
            G.add_edge(node, connected_node)
    
    # Identify the node with the most connections
    max_connected_node = max(connections, key=lambda x: len(connections[x]))
    
    # Connect nodes with zero connections to the node with the most connections
    for node, connected_nodes in connections.items():
        if not connected_nodes:
            G.add_edge(node, max_connected_node)
    
    return G