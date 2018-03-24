import json
import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
# set_U = set()
set_V = set()


def load_data(data):
    return json.load(open(data, "r"))


def get_set_u(data):
    return set(data.keys())


def get_set_v(data, set_u):
    for user in set_u:
        for elem in data[user]:
            set_V.update(elem.keys())


def setup_nodes(graph, set_user, set_repo):
    graph.add_nodes_from(set_user)
    graph.add_nodes_from(set_repo)


def setup_edges(data, graph, set_user, set_repos):
    for user in set_user:
        for repo in set_repos:
            for elem in data[user]:
                if repo in elem:
                    edge = (user, repo)
                    graph.add_edge(*edge)


def draw_graph(graph):
    nx.draw(graph, with_labels=True, font_weight='bold')
    # plt.subplot(122)
    # nx.draw_shell(graph, with_labels=True, font_weight='bold')


def main():
    data = load_data("depth3.json")
    set_U = get_set_u(data)
    print("set_U lenght:", len(set_U))
    get_set_v(data, set_U)
    print("set_V length:", len(set_V))
    setup_nodes(G, set_U, set_V)
    print("graph nodes:", len(G.nodes()))
    setup_edges(data, G, set_U, set_V)
    print("graph edges:", len(G.edges()))
    draw_graph(G)
    plt.show()


main()
