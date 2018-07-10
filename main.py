import networkx as nx
from data_elaboration.network_analysis import run_setup, run_analytical_task, get_coeff_from_net,\
    generate_comparable_graphs, generate_edgelist
from data_elaboration.data_retrieval.get_data import run_crawler
from data_elaboration.net_elaboration import get_csv_from_json
from data_elaboration.community_discovery import run_community_discovery_task
from data_elaboration.epidemic_analysis import get_epidemic_analysis
from data_elaboration.tie_stregth_analysis import run_tie_stregth_analysis
from pprint import pprint

csv_file = "edgelistNx.csv"
# json_file = "/home/andrea/Documenti/Università/Social Network Analysis/sna_github_repos/data_elaboration/luglio_merged.json"


def run_graph_creation_and_analysis():
    graph_crawled = run_setup(csv_file)

    graph_crawled = nx.convert_node_labels_to_integers(graph_crawled)

    # run_community_discovery_task(graph_crawled)

    degree_centrality, edge_bet_centrality = run_analytical_task(graph_crawled)
    # run_tie_stregth_analysis(graph_crawled, degree_centrality, edge_bet_centrality)
    #
    # nodes, p_er, m_ba = get_coeff_from_net(graph_crawled)
    # graph_er, graph_ba = generate_comparable_graphs(nodes, p_er, m_ba)
    # comparable_graph_list = list((graph_er, graph_ba))
    #
    # for graph in comparable_graph_list:
    #     print("____________________________________________________________________________________")
    #     degree_centrality, edge_bet_centrality = run_analytical_task(graph)
    #     run_tie_stregth_analysis(graph, degree_centrality, edge_bet_centrality)
    #
    # # genera file json che descriva il network
    # # generate_edgelist(comparable_graph_list)
    #
    # return graph_crawled, graph_er, graph_ba


def main():
    # run_crawler()
    # get_csv_from_json(json_file)
    graph_crawled, graph_er, graph_ba = run_graph_creation_and_analysis()


    graph_list = list((graph_crawled, graph_er, graph_ba))
    comp_list = list()
    print("________________________________________________________________________________________")
    print("Community Discovery Task --------")
        # for graph in graph_list:
        #     comp_list.append(run_community_discovery_task(graph))


    # get_epidemic_analysis(graph_crawled)

main()


# workflow:
# 0 crawler (task1)
# 1 creazione graph_crawled
# 2 analisi run_analytical_task su graph_crawleed (task1)
# 3 analisi tie_strength  (task 3.c)
# 3 crazione modelli sintetici p=0.000241437356073 e m=2.87636394158
# 4 analisi modello + tie_stregth per i modelli sintetici (task2)
# 5 per ogni modello (crawler + sintetici) analisi Community Discovery (task3.a)
# 6 per crawled run epidemic_analysis (task3.b)
