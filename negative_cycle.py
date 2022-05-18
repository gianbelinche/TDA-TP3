from math import inf

def __find_negative_cycle_node(costs, neighbours, edges, predecessor):
    """
    Recibe un diccionario para almacenar los costos, un diccionario de vecinos, 
    un diccionario de aristas con su capacidad y costo y un diccionario para
    almacenar los predecesores.

    Ejecuta el algoritmo de Bellman-Ford con una iteración extra para
    determinar si existe al menos un ciclo negativo en el grafo.

    Devuelve el primer nodo encontrado que se modifica en caso de existir
    un ciclo negativo o None en caso que no exista ciclo negativo.
    """
    for n in range(len(neighbours)):
        modified = False
        for node in neighbours:
            if costs[node] < inf:
                for neighbour in neighbours[node]:
                    # (capacity, cost)
                    enabled = edges[(node, neighbour)][2]

                    # No se visitan las aristas desactivadas
                    if not enabled: continue
                    
                    cost = edges[(node, neighbour)][1]
                    if cost + costs[node] < costs[neighbour]:
                        modified = True
                        costs[neighbour] = cost + costs[node]
                        predecessor[neighbour] = [node, cost]
                        if n == len(neighbours) - 1:
                            return neighbour

        if not modified:
            return None
    
    raise Exception("Unreachable section has been reached")

def find_negative_cycle(initial, neighbours, edges):
    """
    Recibe el nodo inicial, un diccionario de vecinos y un diccionario de
    aristas con su capacidad y costo.
    
    En caso de existir ciclo negativo, devuelve una lista con los nodos
    pertenecientes a dicho ciclo. En caso contrario,
    devuelve una lista vacía.
    """
    costs = dict()
    predecessor = dict()

    for node in neighbours:
        costs[node] = inf
    costs[initial] = 0

    cycle_target = __find_negative_cycle_node(costs, neighbours, edges, predecessor)
    if not cycle_target:
        return []

    # Tomamos un camino de largo n, donde debe encontrarse
    # al menos una instancia del ciclo negativo
    negative_cycle = []
    found = dict()
    for i in range(len(neighbours) + 1):
        negative_cycle.append(cycle_target)

        if cycle_target in found:
            negative_cycle = negative_cycle[found[negative_cycle[i]]:i]
            break
        else:
            found[cycle_target] = i

        cycle_target = predecessor[cycle_target][0]

    return negative_cycle[::-1]
