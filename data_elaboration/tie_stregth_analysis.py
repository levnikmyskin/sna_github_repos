import networkx as nx


def run_tie_stregth_analysis(graph, degree_centrality, edge_bet_centrality):
    print("_____________________________________________________________________")
    print("Tie Stregth Analysis: ")

    graph_copy_1 = graph.copy()
    grah_copy_2 = graph.copy()

    remove_by_degree_cen(graph_copy_1, degree_centrality)
    print("\n")
    remove_by_bet_cen(grah_copy_2, edge_bet_centrality)


def remove_by_degree_cen(graph, degree_centrality):
    print("Number of Connected Components through time wrt Degree Centrality")

    number_cc_degree = list()
    sorted_degree = sorted(degree_centrality.items(), key=lambda t: t[1], reverse=True)

    number_cc_degree.append(nx.number_connected_components(graph))

    for elem in sorted_degree:
        graph.remove_node(elem[0])
        number_cc_degree.append(nx.number_connected_components(graph))

    print(number_cc_degree)


def remove_by_bet_cen(graph, edge_bet_centrality):
    print("Number of Connected Components through time wrt Edge Bet cent")

    number_cc_edge = list()
    sorted_edge_bet = sorted(edge_bet_centrality.items(), key=lambda t: t[1], reverse=True)

    number_cc_edge.append(nx.number_connected_components(graph))

    for elem in sorted_edge_bet:
        if graph.has_edge(elem[0][0], elem[0][1]):
            graph.remove_edge(elem[0][0], elem[0][1])
            number_cc_edge.append(nx.number_connected_components(graph))
        else:
            continue

    print(number_cc_edge)
