from math import inf

def augment_path(rproperties, negative_cycle):
	bottleneck = inf
	for i in range(len(negative_cycle)):
		origin = negative_cycle[i]
		goal = negative_cycle[(i + 1) % len(negative_cycle)]
		bottleneck = min(bottleneck, rproperties[origin, goal])

	for i in range(len(negative_cycle)):
		origin = negative_cycle[i]
		goal = negative_cycle[(i + 1) % len(negative_cycle)]
		rproperties[origin, goal][0] -= bottleneck
		rproperties[goal, origin][0] += bottleneck
