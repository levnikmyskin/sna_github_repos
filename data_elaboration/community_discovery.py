from networkx.algorithms import community
from networkx.algorithms.community import k_clique_communities
from community import community_louvain
import demon as d
import pquality
from nf1 import NF1


def get_girvan_newman(graph, iteration):
    gn_hierarchy = community.girvan_newman(graph)

    for x in range(iteration):
        coms_gn = [tuple(x) for x in next(gn_hierarchy)]

    return coms_gn


def get_k_clique(graph, k):
    clique = list(k_clique_communities(graph, k))

    return clique

# TODO: capire differenza fra due modelli label_prop
def get_label_prop(graph):
    # comm_generator = community.label_propagation_communities(graph)
    comm_generator = community.asyn_lpa_communities(graph)
    comm_generator = list(comm_generator)

    return comm_generator

def get_louvain(graph):
    partition = community_louvain.best_partition(graph, weight="weight")

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
    # TODO: ma questa loading bar vorrei toglierla ma non ho voglia di cercare come...
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
    clique_part = get_k_clique(graph, 3)
    girv_part = get_girvan_newman(graph, 10)
    label_part = get_label_prop(graph)
    louv_part = get_louvain(graph)
    demon_part = get_demon(graph)

    print_results(clique_part, girv_part, label_part, louv_part, demon_part)
    run_pquality_test(graph, clique_part, girv_part, label_part, louv_part, demon_part)

    partition_list = list(((clique_part, "Clique_part"), (girv_part, "Girv_part"), (label_part, "Label_part"),
                           (louv_part, "Louv_part"), (demon_part, "Demon_part")))

    run_nf1_evaluation(partition_list)

    return partition_list


def run_nf1_evaluation(partition_list):
    for partition in partition_list:
        _partition_list_copy = partition_list.copy()
        _partition_list_copy.remove(partition)
        index = partition_list.index([partition][0])

        for comparable_partition in _partition_list_copy[index:]:
            nf = NF1(partition[0], comparable_partition[0])
            res = nf.summary()

            print(f"Comparison between {partition[1]} and {comparable_partition[1]}:")
            print(res["scores"])
            print("____________________________________________________")

            # print("Details:")
            # print("\n")
            # print(res["details"])
            # print("____________________________________________________")
            # print("\n")


def run_pquality_test(graph, clique_part, girv_part, label_part, louv_part, demon_part):
    print("\n")
    print("Clique Evaluation")
    get_partition_quality(graph, clique_part)
    print("____________________________________________________________")

    print("\n")
    print("Girvan-Newman Evaluation")
    get_partition_quality(graph, girv_part)
    print("____________________________________________________________")

    print("\n")
    print("Label Propagation Evaluation")
    get_partition_quality(graph, label_part)
    print("____________________________________________________________")

    print("\n")
    print("Louvain Evaluation")
    get_partition_quality(graph, louv_part)
    print("____________________________________________________________")

    print("\n")
    print("Demon Evaluation")
    get_partition_quality(graph, demon_part)
    print("____________________________________________________________")


