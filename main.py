from math import inf
from copy import deepcopy
import negative_cycle as nc
import augment_path as ap
import sys
import edmonds_karp as ek

def read_graph_file(path):
	neighbors = dict()
	properties = dict()	

	with open(path) as file:
		source = file.readline().strip()
		target = file.readline().strip()
		C = 0
		for line in file:
			node1, node2, cost, capacity = line.strip().split(',')
			properties[(node1, node2)] = (int(capacity), int(cost), True)
			if node1 == source:
				C += int(capacity)
			if node1 in neighbors:
				neighbors[node1].append(node2)
			else:
				neighbors[node1] = [node2]
	
	return source, target, neighbors, properties, C

def residual_graph(source, target, rneighbors, rproperties, C):
	neighbors  = deepcopy(rneighbors)

	rneighbors['source'] = [source]
	rproperties[('source', source)] = (C, 0, True)

	rneighbors[target] = ['target']
	rproperties[(target, 'target')] = (C, 0, True)

	for node, nlist in neighbors.items():
		for neighbor in nlist:
			if neighbor in rneighbors:
				rneighbors[neighbor].append(node)
			else:
				rneighbors[neighbor] = [node]
			rproperties[(neighbor, node)] = (0, -rproperties[(node, neighbor)][1], True)
	
	rneighbors["target"] = [target]
	rproperties[("target",target)] = (0,0, True)
	if source in rneighbors:
		rneighbors[source].append("source")
	else:
		rneighbors[source] = ["source"]
	rproperties[(source,"source")] = (0,0, True)

	return 'source', 'target'

def solve_flights(path):
	source, target, rneighbors, rproperties, C = read_graph_file(path)
	rsource, rtarget = residual_graph(source, target, rneighbors, rproperties, C)

	maximum_flow = ek.edmonds_karp(rneighbors, rproperties,rsource, rtarget)
	
	negative_cycle = nc.find_negative_cycle(rsource, rneighbors, rproperties)
	while len(negative_cycle) > 0:
		ap.augment_path(rproperties, negative_cycle)
		negative_cycle = nc.find_negative_cycle(rsource, rneighbors, rproperties)


	minimum_cost = 0
	for (origin, goal), (capacity, cost, enabled) in rproperties.items():
		if cost > 0:
			minimum_cost += cost*rproperties[goal, origin][0]

	return maximum_flow, minimum_cost

def main():
    if len(sys.argv) < 2:
        print("Error: faltan parámetros.")
        print("Uso: main.py <ruta_archivo>")
        return

    maximum_flow, minimum_cost = solve_flights(sys.argv[1])
    print('Cantidad de personas maximas:', maximum_flow)
    print('Costo total mínimo:', minimum_cost)

main()
