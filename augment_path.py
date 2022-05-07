from math import inf

def augment_path(rproperties, negative_cycle):
	bottleneck = inf
	for i in range(len(negative_cycle)):
		origin = negative_cycle[i]
		goal = negative_cycle[(i + 1) % len(negative_cycle)]
		bottleneck = min(bottleneck, rproperties[origin, goal][0])	
		if bottleneck == 0:
			rproperties[origin,goal] = (rproperties[origin,goal][0], rproperties[origin,goal][1], False)
			return

	for i in range(len(negative_cycle)):
		origin = negative_cycle[i]
		goal = negative_cycle[(i + 1) % len(negative_cycle)]
		rproperties[origin, goal] = (rproperties[origin,goal][0] - bottleneck, rproperties[origin,goal][1], True)
		rproperties[goal, origin] = (rproperties[goal,origin][0] + bottleneck, rproperties[goal,origin][1], True)
	
