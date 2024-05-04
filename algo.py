

from collections import defaultdict

class Node:
    def __init__(self, node_type, name):
        self.node_type = node_type
        self.name = name
        self.connections = {}

def construct_drug_retargeting_graph(disease_protein_map, drug_protein_map):
    graph = {}

    for disease, proteins in disease_protein_map.items():
        if disease not in graph:
            graph[disease] = Node("Disease", disease)
        for protein in proteins:
            if protein not in graph:
                graph[protein] = Node("Protein", protein)
            graph[disease].connections[protein] = 0

    for drug, protein_list in drug_protein_map.items():
        if drug not in graph:
            graph[drug] = Node("Drug", drug)
        for protein, effectiveness in protein_list.items():
            if protein not in graph:
                graph[protein] = Node("Protein", protein)
            graph[drug].connections[protein] = effectiveness

    return graph

def find_potential_targets(graph, drug):
    if drug not in graph:
        return []
    
    targets = set()
    visited_proteins = set()
    drug_node = graph[drug]
    
    def dfs(node, weight_so_far):
        if node.node_type == "Disease":
            targets.add(node.name)
            return
        for protein, effectiveness in node.connections.items():
            if protein not in visited_proteins:
                visited_proteins.add(protein)
                dfs(graph[protein], weight_so_far * effectiveness)
    
    dfs(drug_node, 1)
    return list(targets)
