from math import inf
from copy import deepcopy
import negative_cycle as nc
import augment_path as ap
import sys

def read_graph_file(path):
    neighbors = dict()
    properties = dict()

    with open(path) as file:
        source = file.readline().strip()
        target = file.readline().strip()
        for line in file:
            node1, node2, cost, capacity = line.strip().split(',')
            properties[(node1, node2)] = (int(capacity), int(cost))
            if node1 in neighbors:
                neighbors[node1].append(node2)
            else:
                neighbors[node1] = [node2]

    return source, target, neighbors, properties

def residual_graph(source, target, neighbors, properties):
	rneighbors  = deepcopy(neighbors)
	rproperties = deepcopy(properties)

	rneighbors['source'] = [source]
	rproperties[('source', source)] = (inf, 0)

	rneighbors[target] = ['target']
	rproperties[(target, 'target')] = (inf, 0)

	for node, nlist in neighbors.items():
		for neighbor in nlist:
			if neighbor in neighbors:
				rneighbors[neighbor].append(node)
			else:
				rneighbors[neighbor] = [node]
			rproperties[(neighbor, node)] = (0, -rproperties[(node, neighbor)][1])

	return 'source', 'target', rneighbors, rproperties

def solve_flights(path):
	source, target, neighbors, properties = read_graph_file(path)
	rsource, rtarget, rneighbors, rproperties = residual_graph(source, target, neighbors, properties)

	maximum_flow = ff.ford_fulkerson(rsource, rtarget, rneighbors, rproperties)

	negative_cycle = nc.find_negative_cycle_node(rsource, rneighbors, rproperties)
	while len(negative_cycle) > 0:
		ap.augment_path(rneighbors, rproperties, negative_cycle)
		negative_cycle = nc.find_negative_cycle_node(rsource, rneighbors, rproperties)

	minimum_cost = 0
	for (origin, goal), value in rproperties.items():
		minimum_cost += value[1]*rproperties[goal, origin][0]

	return maximum_flow, minimum_cost

def main():
    if len(sys.argv) < 2:
        print("Error: faltan parámetros.")
        print("Uso: main.py <ruta_archivo>")
        return

    maximum_flow, minimum_cost = solve_flights(sys.argv[1])
    print('Cantidad de personas maximas: ', maximum_flow)
    print('Costo total mínimo:', maximum_cost)

main()
