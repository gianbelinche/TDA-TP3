from math import inf
from copy import deepcopy
import negative_cycle as nc
import augment_path as ap
import edmonds_karp as ek
import sys

SOURCE_TAG = 'source'
TARGET_TAG = 'target'

def read_graph_file(path):
	"""
	Recibe la ruta del archivo y construye el grafo de acuerdo a lo especificado.
	Retorna el nodo fuente, sumidero, un diccionario de adyacencia y un diccionario de
	propiedades de aristas (capacidad,costo) y la suma de las capacidades salientes de la fuente.
	"""
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
	"""
	Recibe un nodo fuente y sumidero. Asi como, un grafo en forma de diccionario de adyacencia, un diccionario de
	propiedades de aristas (capacidad,costo) y la suma de las capacidades salientes de la fuente.
	Construye el grafo residual sobre las estructuras recibidas (in-place) y retorna la fuente y sumidero ficticia.
	"""

	#Necesario para iterar luego
	neighbors = deepcopy(rneighbors)

	rneighbors[SOURCE_TAG] = [source]
	rproperties[(SOURCE_TAG, source)] = (C, 0, True)

	rneighbors[target] = [TARGET_TAG]
	rproperties[(target, TARGET_TAG)] = (C, 0, True)

	for node, nlist in neighbors.items():
		for neighbor in nlist:
			if neighbor in rneighbors:
				rneighbors[neighbor].append(node)
			else:
				rneighbors[neighbor] = [node]
			rproperties[(neighbor, node)] = (0, -rproperties[(node, neighbor)][1], True)
	
	rneighbors[TARGET_TAG] = [target]
	rproperties[(TARGET_TAG,target)] = (0,0, True)
	if source in rneighbors:
		rneighbors[source].append(SOURCE_TAG)
	else:
		rneighbors[source] = [SOURCE_TAG]
	rproperties[(source,SOURCE_TAG)] = (0,0, True)

	return SOURCE_TAG, TARGET_TAG

def solve_flights(path):
	"""
	Recibe la ruta del archivo de vuelos y retorna la máxima cantidad de personas que
	pueden volar y el costo de transportarlos.
	"""
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
