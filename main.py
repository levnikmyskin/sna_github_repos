import networkx as nx
from data_elaboration.network_setup import run_setup, run_analytical_task, get_coeff_from_net,\
    generate_comparable_graphs, generate_edgelist
from data_elaboration.data_retrieval.get_data import run_crawler
from data_elaboration.net_elaboration import get_json_to_csv
from data_elaboration.community_discovery import run_community_discovery_task
from data_elaboration.epidemic_analysis import do_epidemic_analysis

csv_file = "CSVlabel.csv"
json_file = "luglio2.json"


def run_graph_creation_and_analysis():
    graph_crawled = run_setup(csv_file)
    run_analytical_task(graph_crawled)

    nodes, p_er, m_ba = get_coeff_from_net(graph_crawled)
    graph_er, graph_ba = generate_comparable_graphs(nodes, p_er, m_ba)
    comparable_graph_list = list((graph_er, graph_ba))

    for graph in comparable_graph_list:
        print("____________________________________________________________________________________")
        run_analytical_task(graph)

    return graph_crawled, graph_er, graph_ba

    # genera file json che descriva il network
    # generate_edgelist(comparable_graph_list)


def main():
    # run_crawler()
    # get_json_to_csv(json_file)
    graph_crawled, graph_er, graph_ba = run_graph_creation_and_analysis()

    crawled_int = nx.convert_node_labels_to_integers(graph_crawled)
    graph_list = list((crawled_int, graph_er, graph_ba))
    for graph in graph_list:
        run_community_discovery_task(graph)

    do_epidemic_analysis(graph_crawled)


main()

