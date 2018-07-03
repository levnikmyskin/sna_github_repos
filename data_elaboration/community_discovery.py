import networkx as nx
from networkx.algorithms import community
from networkx.algorithms.community import k_clique_communities
import itertools
from community import community_louvain
import demon as d

# TODO: capire! Se le reti con cui compariamo vengono generate ogni volta, queste saranno sempre leggermente diverse quindi direi
# che è necessario - una volta create - salvare come edgelist e poi ricrearle sempre a partire da edgelist in modo che siano sempre uguali...


# TODO: far sì che qui vengano importati le reti impostate in network_setup. Per velocità adesso utilizzo delle reti generate random
graph_ba = nx.barabasi_albert_graph(100, 5, seed=None)


def get_girvan_newman(graph, iteration):
    girvan_list = list()
    comm_generator = community.girvan_newman(graph)
    limited = itertools.takewhile(lambda t: len(t) <= iteration, comm_generator)
    for communities in limited:
        girvan_list.append(tuple(sorted(c) for c in communities))

    return girvan_list


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


def main():
    clique = get_k_clique(graph_ba, 3)
    girv_part = get_girvan_newman(graph_ba, 5)
    label_part = get_label_prop(graph_ba)
    louv_part = get_louvain(graph_ba)
    demon_part =  get_demon(graph_ba)

    print_results(clique, girv_part, label_part, louv_part, demon_part)



main()