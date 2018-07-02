import json
from pprint import pprint
import networkx as nx
import csv
import collections

data = json.load(open("depth4.json", "r"))


def get_repo_user_dict(data):
    repo_dict = dict()
    for user, repoList in data.items():
        for repo in repoList:
            for repoName, val in repo.items():
                a = repo_dict.setdefault(repoName, set())
                # a.append((user, val["commits"]))
                # ho rimosso i pesi per semplicità
                a.add((user, ))

    return repo_dict


def get_coll_dict(repo_dict):
    coll_dict = dict()
    for repoName, userList in repo_dict.items():
        for user in userList:
            user_collaborators = coll_dict.setdefault(user[0], [])
            _userList = userList.copy()
            _userList.remove(user)
            for collaborator in _userList:
                user_collaborators.append(collaborator)

    return coll_dict


def create_network_from_json(coll_dict):
    graph = nx.Graph()
    for user, userList in coll_dict.items():
        graph.add_edges_from(([(user, collaborator) for collaborator in userList]))

    return graph


def create_network_from_csv(csvfile):
    graph = nx.Graph()
    with open(csvfile, "r") as csvfile:
        dataList = list(csv.reader(csvfile, delimiter=";"))
        for elem in dataList:
            graph.add_edge(elem[0], elem[1])

    return graph


def create_csv(coll_dict):
    with open("testCSV.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=";", quotechar="|", quoting=csv.QUOTE_MINIMAL)
        for userName, collaboratorList in coll_dict.items():
            for collaborator in collaboratorList:
                writer.writerow([userName, collaborator[0]])


csvfile = "10k.csv"
repo_dict = get_repo_user_dict(data)
coll_dict = get_coll_dict(repo_dict)
#create_csv(coll_dict)
# graph = create_network_from_json(coll_dict)

graph = create_network_from_csv(csvfile)
nodes = graph.number_of_nodes()
edges = graph.number_of_edges()
con_components = nx.number_connected_components(graph)
density = nx.density(graph)
degree_centrality = nx.degree_centrality(graph)


number_of_nodes = 0

for component in nx.connected_component_subgraphs(graph):
    if component.number_of_nodes() > 1000:
        max_comp = component
        number_of_nodes = max_comp.number_of_nodes()
    else:
        continue

shortest_path = nx.shortest_path_length(max_comp)
closeness_centrality = nx.closeness_centrality(max_comp)
sorted_closeness_centrality = sorted(closeness_centrality.items(), key=lambda t:t[1], reverse=True)
edge_betweenness = nx.edge_betweenness_centrality(max_comp)
sorted_edge_betweenness = sorted(edge_betweenness.items(), key=lambda t:t[1], reverse=True)
degree_centrality_comp = nx.degree_centrality(max_comp)
sorted_degree_centrality = sorted(degree_centrality_comp.items(), key=lambda t:t[1], reverse=True)


degree_sequence = sorted([d for n, d in graph.degree()], reverse=True)
degreeCount = collections.Counter(degree_sequence)

degreeList = list()
for node in graph.nodes():
    degreeList.append(graph.degree(node))



print("--- Network Analysis:")
print("Nodes: " + str(nodes))
print("Edges: " + str(edges))
print("Density: " + str(density))
print("Max Degree: " + str(max(degreeList)))

print("Connected Components: " + str(con_components))
print("Graph Avg Degree: " + str(2*edges/nodes))
print("Edge Probability: " + str(2*edges/(nodes * (nodes-1))))
print("Max Comp Diameter: " + str(nx.diameter(max_comp)))
print("Max Comp Average Clustering: " + str(nx.average_clustering(max_comp)))
print("Max Comp Shortest Path: " + str(shortest_path))

# print("Max Degree Centrality: " + str((degree_centrality)))
# pprint(max(degree_centrality))

print("Max Comp Degree Centrality: " + str(list(sorted_degree_centrality)[0]))
print("Max Comp Closeness Centrality: " + str(list(sorted_closeness_centrality)[0]))
print("Max Comp Edge Betweenness: " + str(list(sorted_edge_betweenness)[0]))

# print("Degree Distribution: " + str((degreeCount)))


