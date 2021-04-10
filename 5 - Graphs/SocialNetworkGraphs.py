# !/usr/bin/env python3
import snap
import pprint

from os import path

graph_path = path.join(path.dirname(__file__), 'social_networks/links2.edges')

###########################################################################################
# UNDIRECTED GRAPH
###########################################################################################
(undirected_graph, ug_map) = snap.LoadEdgeListStr(snap.TUNGraph, graph_path, 0, 1, Mapping = True)
ugraph_diameter = undirected_graph.GetBfsFullDiam(100, False)

undirected_degrees = undirected_graph.GetDegSeqV(False)
undirected_degrees_dictionary = {id: undirected_degrees[id] for id in range(0, len(undirected_degrees))}
undirected_degrees_sorted = sorted(undirected_degrees_dictionary.items(), key=lambda x: x[1], reverse=True)

top10_nodes_unidirect= []

for id, degrees in undirected_degrees_sorted[:10]:
    top10_nodes_unidirect.append(f"Node {ug_map.GetKey(id)} has degree {degrees}")

top_300_nodes_ids = [id for id, degrees in undirected_degrees_sorted[:300]]

undirected_graph.DelNodes(top_300_nodes_ids)
updated_ugraph_diameter = undirected_graph.GetBfsFullDiam(100, False)

###########################################################################################
# DIRECTED GRAPH
###########################################################################################

(directed_graph, g_map) = snap.LoadEdgeListStr(snap.TNGraph, graph_path, 0, 1, Mapping = True)
graph_diameter = directed_graph.GetBfsFullDiam(100, True)

in_degree, out_degree = directed_graph.GetDegSeqV(True)

directed_graph_degrees = zip(range(0, len(in_degree)), in_degree, out_degree)
directed_graph_degrees_sorted = sorted(directed_graph_degrees, key=lambda tup: tup[1], reverse=True)

top10_nodes_direct = []
for node in directed_graph_degrees_sorted[:10]:
  top10_nodes_direct.append(f"Node {ug_map.GetKey(node[0])} has in-degree {node[1]} and out-degree {node[2]}")

top_300_in_ids = [id for id, _, _ in directed_graph_degrees_sorted[:300]]

directed_graph.DelNodes(top_300_nodes_ids)

updated_graph_diameter = directed_graph.GetBfsFullDiam(100, True)

########################################################
# SUMMARY
########################################################

print("SUMMARY:")
print("--------------------------------------")
print("UNDIRECTED GRAPH:")
print("TOP 10 NODES:")
pprint.pp(top10_nodes_unidirect)
print(f"DIAMETER: Initial: {ugraph_diameter} Updated: {updated_ugraph_diameter}")
print("--------------------------------------")
print("DIRECTED GRAPH:")
print("TOP 10 NODES:")
pprint.pp(top10_nodes_direct)
print(f"DIAMETER: Initial: {graph_diameter} Updated: {updated_graph_diameter}")