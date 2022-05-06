import math

def Ford_Fulkerson(neighbors,capacitys,source,target):
    max_flow = 0
    finished = False
    while not finished:
        bottleneck = math.inf
        path = []
        visited = set()
        actual = source
        reached_target,bottleneck = dfs(neighbors,capacitys,actual,target,visited,path,False,bottleneck)
        if reached_target:
            max_flow += bottleneck
            for first,second in path:
                capacitys[(first,second)] = (capacitys[(first,second)][0] - bottleneck,capacitys[(first,second)][1]) 
                capacitys[(second,first)] = (capacitys[(second,first)][0] + bottleneck,capacitys[(second,first)][1])
        else:
            break
    return max_flow


def dfs(neighbors,capacitys,actual,target,visited,path,reached_target,bottleneck):
    visited.add(actual)
    if actual == target:
        return True,bottleneck
    for ng in neighbors[actual]:
        if ng not in visited and capacitys[(actual,ng)][0] > 0:
            bottleneck2 = bottleneck
            if capacitys[(actual,ng)][0] < bottleneck:
                bottleneck = capacitys[(actual,ng)][0]
            ret = dfs(neighbors,capacitys,ng,target,visited,path,reached_target,bottleneck)
            reached_target = ret[0]
            if ret[0]:
                path.append((actual,ng))
                bottleneck = ret[1]
                break
            else:
                bottleneck = bottleneck2
    return reached_target,bottleneck


neighbors = {"A" : ["B","C"], "B" : ["A"],"C":["D","A"], "D" : ["C"]}
capacitys = {("A","B") : (10,0),("A","C") : (5,0), ("B","A") : (0,0), ("C","D"): (1,0), ("C","A") : (0,0), ("D","C"): (0,0)}
source = "A"
target = "D"

print(Ford_Fulkerson(neighbors,capacitys,source,target))

     

        


