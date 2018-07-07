import json
import collections
from networkx import Graph

data = json.load(open("data2135.json", "r"))


def get_most_freq_lang(data):
    language_list = list()

    for _, repo_list in data.items():
        for repo in repo_list:
            for _, repoinfo in repo.items():
                language_list.append(repoinfo["language"])

    c = collections.Counter(language_list)
    print(c.most_common())


def control_depth(data):
    for user, repo_list in data.items():
        visited_repo = list()
        for repo in repo_list:
            if repo in visited_repo:
                print("WARNING", repo)
                quit()
            visited_repo.append(repo)


def prepare_data_for_rust(network):
    nodes = list(network.nodes)
    adj = network.adj
    radj = list()
    for k, v in adj.items():
        n = list()
        for v2 in v.keys():
            n.append(v2)
        radj.append((k, n))
    return nodes, radj



def merge_dictionaries(first_dict, second_dict):
    if len(first_dict) > len(second_dict):
        return _merge_dicts(first_dict, second_dict)
    else:
        return _merge_dicts(second_dict, first_dict)


def _merge_dicts(f_dict, s_dict):
    visited_users = set()
    for user, repos in f_dict.items():
        visited_users.add(user)
        s_repo = s_dict.get(user)
        if not s_repo:
            continue
        merged_repos = repos + s_repo
        visited = set()
        final_repos = list()
        for mr in merged_repos:
            key = next(iter(mr))
            if key not in visited:
                visited.add(key)
                final_repos.append(mr)
        f_dict[user] = final_repos

    for user, repos in s_dict.items():
        if user not in visited_users:
            f_repo = f_dict.get(user)
            if not f_repo:
                # if s_dict user doesn't exist in f_dict, we can simply copy/paste it
                f_dict[user] = repos
                continue
            merged_repos = repos + f_repo
            visited = set()
            final_repos = list()
            for mr in merged_repos:
                key = next(iter(mr))
                if key not in visited:
                    visited.add(key)
                    final_repos.append(mr)
            f_dict[user] = final_repos

    return f_dict


def get_rust_shortpath():
    import networkx as nx
    import networkxrust
    n = nx.fast_gnp_random_graph(200, 0.3, directed=False)
    nodes, radj = prepare_data_for_rust(n)
    return networkxrust.shortest_path_length(nodes, radj)
