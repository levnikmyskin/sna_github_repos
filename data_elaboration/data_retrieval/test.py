from typing import Dict
import requests
import json
import time
from pprint import pprint

CONTRIBUTORS_ENDPOINT = "https://api.github.com/repos/{}/{}/stats/contributors"
REPOS_ENDPOINT = "https://api.github.com/users/{}/repos"
user_dict = dict()
visited_repos = set()
headers_sna = {'socialNetworkAnalysis': 'XTfLGSS3'}
t = 2


class Repo:
    __slots__ = ["name", "commits", "language"]

    def __init__(self, name: str, commits: int, language: str):
        self.name = name
        self.commits = commits
        self.language = language


class CustomJsonEncoder(json.JSONEncoder):

    def __init__(self):
        super(CustomJsonEncoder, self).__init__()

    def default(self, o):
        if type(o) == Repo:
            pass
        else:
            super(CustomJsonEncoder, self).default(o)


def get_repo_contributors(owner, repo):
    if repo in visited_repos:
        return
    response = requests.get(CONTRIBUTORS_ENDPOINT.format(owner, repo), headers=headers_sna)
    print(response)
    data_json = response.json()
    user_list = list()

    if len(data_json) > 5:
        for i in range(len(data_json) - 5, len(data_json)):
            user_list.append(get_contributor_info(data_json[i]))
    else:
        for elem in data_json:
            user_list.append(get_contributor_info(elem))

    visited_repos.add(repo)
    return user_list


# devo riuscire a prendere le repo dell'utente, restituirla e per ogni repo vedere i primi 5 contributors.
def get_user_repos(user):
    response = requests.get(REPOS_ENDPOINT.format(user), headers=headers_sna)
    print(response)
    repos_json = response.json()
    repo_list = list()

    for elem in repos_json:
        repo_list.append(get_repos_info(elem))

    return repo_list


def get_contributor_info(contributor_dic: Dict):
    return contributor_dic["author"]["login"], contributor_dic["total"]


def get_repos_info(repos_dic: Dict):
    return repos_dic['name'], repos_dic['language']


def run_from_data(data, repo_name, language):
    for user in data:
        username = user[0]
        # The method setdefault() is similar to get(), but will set dict[key]=default if key is not already in dict.
        repos = user_dict.setdefault(username, [])
        repos.append(Repo(repo_name, user[1], language))


def save_data(data, file):
    json.dump(data, open(file, "w"))


def main():
    data = get_repo_contributors("torvalds", "linux",)
    save_data(data, "salvo_da_funzione.json")
    # data = json.load(open("salvo_da_funzione.json", "r"))

    # DEPTH 0 - i primi 5 contributors della repo di partenza(linux)
    run_from_data(data, "linux", "C")

    # DEPTH 1 - i primi 5 contributors di ogni repo che appartiene ai 5 users selezionati a DEPTH 0 (/depth precedente)
    # gli user sono quelli presenti nel dizionario user_dict, quindi per ogni user nel dizionario chiamo get_user_repo
    # per ogni repo, chiamo run_from_data.
    # TODO possibilità di controllare la depth della funzione
    # TODO verificare non esistenza problemi con repo vuote o con autore singolo
    _user_dict_copy = user_dict.copy()
    for user in _user_dict_copy:
        print(user)
        repos_data = get_user_repos(user)
        for repo in repos_data:
            data = get_repo_contributors(user, repo[0])
            # Timer di attesa t per richiesta API github
            time.sleep(t)
            run_from_data(data, repo[0], repo[1])
        print(len(user_dict))
        pprint(user_dict)
    save_data(user_dict, "test_crawler.json")


main()

