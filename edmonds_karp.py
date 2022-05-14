from math import inf

def edmonds_karp(neighbors,properties,source,target):
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
    path = []
    actual = predecessor[target]
    bottleneck = inf 
    while actual != predecessor[actual]:
        path.append(actual)
        bottleneck = min(bottleneck, properties[predecessor[actual], actual][0])
        actual = predecessor[actual]
    return path[::-1], bottleneck

def bfs(neighbors,properties,actual,target):
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
