from math import inf
from copy import deepcopy
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

	print(neighbors)
	print(properties)

	print(rneighbors)
	print(rproperties)

def main():
    if len(sys.argv) < 2:
        print("Error: faltan parámetros.")
        print("Uso: main.py <ruta_archivo>")
        return

    solve_flights(sys.argv[1])

main()
