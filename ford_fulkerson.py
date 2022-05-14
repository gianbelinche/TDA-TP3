from math import inf

def ford_fulkerson(neighbors,properties,source,target):
    max_flow = 0
    path, bottleneck = bfs(neighbors,properties,actual,target)

    while len(path) != 0:
        max_flow += bottleneck
        for first,second in path:
            properties[(first,second)] = (properties[(first,second)][0] - bottleneck,properties[(first,second)][1], True) 
            properties[(second,first)] = (properties[(second,first)][0] + bottleneck,properties[(second,first)][1], True)
        path, bottleneck = bfs(neighbors,properties,actual,target)    
    return max_flow

def _build_path(predecessor, properties, target):
    path = []
    actual = predecessor[target]
    bottleneck = inf 
    while actual != predecessor[actual]:
        path.append(actual)
        bottleneck = min(bottleneck, properties[predecessor[actual], actual][0])
        actual = predecessor[target]
    return path[::-1], bottleneck

def bfs(neighbors,properties,actual,target):
    pending = []
    predecessor = {}
    predecessor[actual] = actual
    for ng in neighbors[actual]:
        pending.append(ng)
        predecessor[ng] = actual

    while(len(pending) != 0):
        actual = pending.pop(0)
        for ng in neighbors[actual]:
            if ng not in predecessor[ng]:
                pending.append(ng)
                predecessor[ng] = actual
                if ng = target:
                    return _build_path(predecessor, properties, target)

    return [], 0
