from math import inf

def edmonds_karp(neighbors,properties,source,target):
    """
    Recibe un diccionario de adyacencia, un diccionario de propiedades de las aristas,
    el nodo fuente y el sumidero.
    Ejecuta el algoritmo de Edmonds-Karp sobre el grafo y retorna su flujo máximo.
    """
    max_flow = 0
    path, bottleneck = bfs(neighbors,properties,source,target)
    while len(path) != 0:
        max_flow += bottleneck 
        for i in range(len(path)-1):
            first = path[i]
            second = path[i + 1]
            properties[(first,second)] = (properties[(first,second)][0] - bottleneck,properties[(first,second)][1], True) 
            properties[(second,first)] = (properties[(second,first)][0] + bottleneck,properties[(second,first)][1], True)
        path, bottleneck = bfs(neighbors,properties,source,target)    
    return max_flow

def _build_path(predecessor, properties, target):
    """
    Función auxiliar de bfs. Recibe un diccionario de predecesores, un diccionario de propiedades de las aristas
    y el nodo objetivo. Retorna el camino en el orden correcto desde el origen hasta el objetivo y el bottleneck.
    """
    path = []
    actual = predecessor[target]
    bottleneck = inf 
    while actual != predecessor[actual]:
        path.append(actual)
        bottleneck = min(bottleneck, properties[predecessor[actual], actual][0])
        actual = predecessor[actual]
    return path[::-1], bottleneck

def bfs(neighbors,properties,actual,target):
    """
    Recibe un diccionario de propiedades de aristas, un diccionario de propiedades de las aristas,
    el nodo fuente y el sumidero. Realiza bfs para encontrar el camino mínimo entre fuente y target,
    retorna una lista con los nodos del camino ordenados y el bottleneck.
    """
    pending = []
    predecessor = {}
    predecessor[actual] = actual
    for neighbor in neighbors[actual]:
        if properties[actual, neighbor][0] > 0:
            pending.append(neighbor)
            predecessor[neighbor] = actual

    while(len(pending) != 0):
        actual = pending.pop(0)
        for neighbor in neighbors[actual]:
            if properties[actual, neighbor][0] > 0 and neighbor not in predecessor:
                pending.append(neighbor)
                predecessor[neighbor] = actual
                if neighbor == target:
                    return _build_path(predecessor, properties, target)

    return [], 0
