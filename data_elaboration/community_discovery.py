import networkx as nx
from networkx.algorithms import community
from networkx.algorithms.community import k_clique_communities
from community import community_louvain
import demon as d
import pquality
import itertools
from nf1 import NF1
import json


def get_girvan_newman(graph, num_components):
    gn_hierarchy = community.girvan_newman(graph)
    coms_gn = tuple()
    for partitions in itertools.islice(gn_hierarchy, num_components):
        coms_gn = partitions

    return coms_gn


def get_k_clique(graph, k):
    clique = list(k_clique_communities(graph, k))

    return clique


def get_label_prop(graph):
    # comm_generator = community.label_propagation_communities(graph)
    comm_generator = community.asyn_lpa_communities(graph)
    comm_generator = list(comm_generator)

    return comm_generator


def get_louvain(graph):
    partition = community_louvain.best_partition(graph)

    list_nodes = list()
    for community in set(partition.values()):
        _list_nodes = list()
        for node in partition.keys():
            if partition[node] == community:
                _list_nodes.append(node)
        list_nodes.append(_list_nodes)

    return list_nodes


def get_demon(graph):
    dm = d.Demon(graph=graph, epsilon=0.25, min_community_size=3)
    # TODO: boh ma che cazzo è sta barra io non la voglio lol
    communities = dm.execute()

    return communities


def print_results(clique, girv_part, label_part, louv_part, demon_part):
    print("K-Clique partitions: " + str(clique))
    print("Girvan-Newman partitions: " + str(girv_part))
    print("Label Propagation partitions: " + str(label_part))
    print("Louvain partitions: " + str(louv_part))
    print("Demon partitions: " + str(demon_part))


def get_partition_quality(graph, partition):
    results = pquality.pquality_summary(graph, partition)
    print(results["Indexes"])


def run_community_discovery_task(graph):
    girv_part = get_girvan_newman(graph, 5)
    json.dump(girv_part, open("girvan.json", 'w'))

    clique_part = get_k_clique(graph, 3)
    json.dump(girv_part, open("clique.json", 'w'))

    label_part = get_label_prop(graph)
    json.dump(girv_part, open("labelpart.json", 'w'))

    louv_part = get_louvain(graph)
    json.dump(girv_part, open("louvain.json", 'w'))

    demon_part = get_demon(graph)
    json.dump(girv_part, open("demon.json", 'w'))

    print_results(clique_part, girv_part, label_part, louv_part, demon_part)

    print("\n")
    print("Clique Evaluation")
    get_partition_quality(graph_ba, clique_part)
    print("____________________________________________________________")

    print("\n")
    print("Girvan-Newman Evaluation")
    get_partition_quality(graph_ba, girv_part)
    print("____________________________________________________________")

    print("\n")
    print("Label Propagation Evaluation")
    get_partition_quality(graph_ba, label_part)
    print("____________________________________________________________")

    print("\n")
    print("Louvain Evaluation")
    get_partition_quality(graph_ba, louv_part)
    print("____________________________________________________________")

    print("\n")
    print("Demon Evaluation")
    get_partition_quality(graph_ba, demon_part)
    print("____________________________________________________________")

