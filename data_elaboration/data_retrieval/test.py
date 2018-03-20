from typing import Dict
import requests
import json
import time
from pprint import pprint

CONTRIBUTORS_ENDPOINT = "https://api.github.com/repos/{}/{}/stats/contributors"
REPOS_ENDPOINT = "https://api.github.com/users/{}/repos"
user_dict = dict()
visited_user = list()
headers_sna = {'socialNetworkAnalysis': 'XTfLGSS3'}
t = 2


class Repo:
    __slots__ = ["name", "commits", "language"]

    def __init__(self, name: str, commits: int, language: str):
        self.name = name
        self.commits = commits
        self.language = language


def get_data(owner, repo):
    # threading.Timer(5.0, get_user_repos).start()
    response = requests.get(CONTRIBUTORS_ENDPOINT.format(owner, repo), headers=headers_sna)
    print(response)
    data_json = response.json()
    data_list = []

    if len(data_json) > 5:
        for i in range(len(data_json) - 5, len(data_json)):
            data_list.append(get_contributor_info(data_json[i]))
    else:
        for elem in data_json:
            data_list.append(get_contributor_info(elem))
    return data_list


# devo riuscire a prendere le repo dell'utente, restituirla e per ogni repo vedere i primi 5 contributors.
def get_user_repos(user):
    # threading.Timer(5.0, get_user_repos).start()
    response = requests.get(REPOS_ENDPOINT.format(user), headers=headers_sna)
    print(response)
    repos_json = response.json()
    data_list = []

    for elem in repos_json:
        data_list.append(get_repos_info(elem))

    return data_list


def get_contributor_info(contributor_dic: Dict):
    return contributor_dic["author"]["login"], contributor_dic["total"], contributor_dic["author"]["repos_url"]


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
    # data = get_data("torvalds", "linux")
    # save_data(data, "salvo_da_funzione.json")
    data = json.load(open("salvo_da_funzione.json", "r"))

    # DEPTH 0 - i primi 5 contributors della repo di partenza(linux)
    run_from_data(data, "linux", "C")

    # DEPTH 1 - i primi 5 contributors di ogni repo che appartiene ai 5 users selezionati a DEPTH 0 (/depth precedente)
    # gli user sono quelli presenti nel dizionario user_dict, quindi per ogni user nel dizionario chiamo get_user_repo
    # per ogni repo, chiamo run_from_data.
    for user in user_dict.copy():
        # se user non è in visited user allora procedi/else continue
        # if user not in visited_user:
        print(user)
        repos_data = get_user_repos(user)
        visited_user.append(user)
        for repo in repos_data:
            data = get_data(user, repo[0])
            # Timer di attesa t per richiesta API github
            time.sleep(t)
            run_from_data(data, repo[0], repo[1])
        print(len(user_dict))
        pprint(user_dict)
    save_data(user_dict, "test_crawler.json")


main()

