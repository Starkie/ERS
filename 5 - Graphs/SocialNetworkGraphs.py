# !/usr/bin/env python3
import snap

from os import path

graph_path = path.join(path.dirname(__file__), 'social_networks/links2.edges')

###########################################################################################
# UNIDIRECTIONAL GRAPH
###########################################################################################
(unidirectional_graph, ug_map) = snap.LoadEdgeListStr(snap.TUNGraph, graph_path, 0, 1, Mapping = True)
ugraph_diameter = unidirectional_graph.GetBfsFullDiam(100, False)


print(f"Diameter unidirectional: {ugraph_diameter}")

unidirectional_degrees = unidirectional_graph.GetDegSeqV(False)
unidirectional_degrees_dictionary = {id: unidirectional_degrees[id] for id in range(0, len(unidirectional_degrees))}
unidirectional_degrees_sorted = sorted(unidirectional_degrees_dictionary.items(), key=lambda x: x[1], reverse=True)

for id, degrees in unidirectional_degrees_sorted:
    print("Node %s has degree %s" % (ug_map.GetKey(id), degrees))

top_300_nodes_ids = [id for id, degrees in unidirectional_degrees_sorted[:300]]

unidirectional_graph.DelNodes(top_300_nodes_ids)
ugraph_diameter = unidirectional_graph.GetBfsFullDiam(100, False)

print(f"Diameter unidirectional: {ugraph_diameter}")


###########################################################################################
# DIRECTED GRAPH
###########################################################################################

(directed_graph, g_map) = snap.LoadEdgeListStr(snap.TNGraph, graph_path, 0, 1, Mapping = True)
graph_diameter = directed_graph.GetBfsFullDiam(100, True)

print(f"Diameter directed: {graph_diameter}")

in_degree, out_degree = directed_graph.GetDegSeqV(True)

directed_graph_degrees = zip(range(0, len(in_degree)), in_degree, out_degree)
directed_graph_degrees_sorted = sorted(directed_graph_degrees, key=lambda tup: tup[1], reverse=True)

for node in directed_graph_degrees_sorted:
  print("Node %s has in-degree %s and out-degree %s" % (ug_map.GetKey(node[0]), node[1], node[2]))

top_300_in_ids = [id for id, _, _ in directed_graph_degrees_sorted[:300]]

directed_graph.DelNodes(top_300_nodes_ids)

graph_diameter = directed_graph.GetBfsFullDiam(100, True)

print(f"Diameter directed: {graph_diameter}")