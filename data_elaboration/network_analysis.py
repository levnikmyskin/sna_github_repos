import networkx as nx
import csv
import collections
import networkxrust
from tools import prepare_data_for_rust, chunks_for_rust


def diameter_from_shortest_paths(shortest_path):
    diameter_list = set()
    for path_list in shortest_path:
        for path_length in path_list[1].values():
            diameter_list.add(path_length)

    return max(diameter_list)


def rust_shortest_path(graph):
    nodes, adj = prepare_data_for_rust(graph)

    e = networkxrust.Elab(nodes, adj[:200])
    for chunk in chunks_for_rust(adj[200:]):
        e.add(chunk)

    e.shortest_path_length()
    return e


def create_network_from_csv(csvfile):
    graph = nx.Graph()
    with open(csvfile, "r") as csvfile:
        data = csv.reader(csvfile, delimiter=";")
        for elem in data:
            graph.add_edge(elem[0], elem[1], weight=float(elem[2]), language=elem[3])

    return graph


def define_max_component(graph):
    cc_comp = max(nx.connected_component_subgraphs(graph), key=len)

    return cc_comp


def centrality_analysis(graph):
    print("BET")
    bet_cen = nx.betweenness_centrality(graph)
    print("EDGE BET")
    edge_bet_cen = nx.edge_betweenness_centrality(graph)
    print("CLO CEN")
    clo_cen = nx.closeness_centrality(graph)

    return bet_cen, edge_bet_cen, clo_cen


def get_sorted_dict(dictionary):
    sort_dict = sorted(dictionary.items(), key=lambda t: t[1], reverse=True)

    return sort_dict


def get_degree_dist(graph):
    degree = list(graph.degree())
    counter = collections.Counter(elem[1] for elem in degree)
    sorted_degree_distribution = counter.most_common()

    return sorted_degree_distribution


def generate_comparable_graphs(nodes, probability, min_degree):
    graph_ER = nx.fast_gnp_random_graph(nodes, probability, directed=False)
    graph_BA = nx.barabasi_albert_graph(nodes, int(min_degree), seed=None)

    return graph_ER, graph_BA


def run_analytical_task(graph):
    max_comp = define_max_component(graph)

    nodes = graph.number_of_nodes()
    print("Nodes: " + str(nodes))

    edges = graph.number_of_edges()
    print("Edges: " + str(edges))

    density = nx.density(graph)
    print("Density: " + str(density))

    degree_centrality = nx.degree_centrality(graph)
    avg_degree = 2*edges/nodes
    con_components = nx.number_connected_components(graph)
    degree_dist = get_degree_dist(graph)
    print("Max Degree: " + str(max(degree_dist)[0]))

    max_comp_nodes = max_comp.order()
    max_comp_edges = max_comp.size()
    avg_clustering_coef = nx.average_clustering(max_comp)
    bet_cen, edge_bet_cen, clo_cen = centrality_analysis(max_comp)
    shortest_path_length = rust_shortest_path(max_comp)
    diameter = diameter_from_shortest_paths(shortest_path_length)

    print_results(nodes, edges, density, degree_dist, max_comp_nodes, max_comp_edges, degree_centrality, avg_degree,
                  con_components, avg_clustering_coef, bet_cen, edge_bet_cen, clo_cen, shortest_path_length, diameter)

    return degree_centrality, edge_bet_cen


def print_results(nodes, edges, density, degree_dist, max_comp_nodes, max_comp_edges, degree_centrality, avg_degree,
                  con_components, avg_clustering_coef, bet_cen, edge_bet_cen,
                  clo_cen, shortest_path_length, diameter):
    print("--- Network Analysis:")
    print("Nodes: " + str(nodes))
    print("Edges: " + str(edges))
    print("Density: " + str(density))
    print("Max Degree: " + str(max(degree_dist)[0]))

    print("Degree Centrality: " + str(get_sorted_dict(degree_centrality)[:5]))
    print("Average Degree: " + str(avg_degree))
    print("Connected Components: " + str(con_components))

    print("\n")
    print("---Biggest Component Analysis:")
    print("Max Comp Nodes: " + str(max_comp_nodes))
    print("Max Comp Edges: " + str(max_comp_edges))
    print("Average Clustering Coefficient: " + str(avg_clustering_coef))
    print("Betweenness Centrality : " + str(get_sorted_dict(bet_cen)[:1]))
    print("Edge Betweenness Centrality : " + str(get_sorted_dict(edge_bet_cen)[:1]))
    print("Closeness Centrality : " + str(get_sorted_dict(clo_cen)[:1]))
    print("Diameter: " + str(diameter))
    print("Shortest Path: " + str(shortest_path_length[:5]))
    print("\n")


def generate_edgelist(comparable_graphs):
    nx.write_edgelist(comparable_graphs[0], "outERdefinitivo.csv", delimiter=";")
    nx.write_edgelist(comparable_graphs[1], "outBAdefinitivo.csv", delimiter=";")


def get_coeff_from_net(graph):
    nodes = graph.number_of_nodes()
    edges = graph.number_of_edges()

    edge_probability_ER = 2 * edges / (nodes * (nodes - 1))
    min_degree_BA = edges / nodes

    return nodes, edge_probability_ER, min_degree_BA


def run_setup(csvfile):
    graph_crawled = create_network_from_csv(csvfile)

    return graph_crawled
