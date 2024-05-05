from collections import defaultdict

class Node:
    def __init__(self, node_type, name):
        self.node_type = node_type
        self.name = name
        self.connections = defaultdict(float)  # Using defaultdict to store effectiveness with default value 0.0

def construct_drug_retargeting_graph(disease_protein_map, drug_protein_map):
    graph = {}

    for disease, proteins in disease_protein_map.items():
        if disease not in graph:
            graph[disease] = Node("Disease", disease)
        for protein in proteins:
            if protein not in graph:
                graph[protein] = Node("Protein", protein)
            # Omitting the effectiveness value, since we want an unweighted graph
            graph[disease].connections[protein] = 0.0

    for drug, protein_list in drug_protein_map.items():
        if drug not in graph:
            graph[drug] = Node("Drug", drug)
        for protein, effectiveness in protein_list.items():
            if protein not in graph:
                graph[protein] = Node("Protein", protein)
            # Adding connection from protein to drug with effectiveness
            graph[protein].connections[drug] = effectiveness
            # Omitting the effectiveness value, since we want an unweighted graph
            graph[drug].connections[protein] = effectiveness

    return graph


def find_potential_targets(graph, protein):
    targets = {}

    if protein in graph:
        for connected_protein_name, effectiveness in graph[protein].connections.items():
            connected_protein = graph[connected_protein_name]
            if connected_protein.node_type == "Drug":
                targets[connected_protein.name] = effectiveness

    return targets
