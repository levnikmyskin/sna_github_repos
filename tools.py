import json
import collections

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


def get_weighted_pairs(coll_dict):
    pass

