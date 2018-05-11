from typing import Dict
import requests
import json
import time
from collections import deque
from data_elaboration.data_retrieval.data_structures import Repo, CustomJsonEncoder

CONTRIBUTORS_ENDPOINT = "https://api.github.com/repos/{}/{}/stats/contributors"
REPOS_ENDPOINT = "https://api.github.com/users/{}/repos"
user_dict = dict()
visited_repos = set()
queue = deque()
# For requests using Basic Authentication or OAuth, you can make up to 5000 requests per hour.
# t_min = 5000/(60*60) = 1.38s
t = 2

_loggedDataContributors = list()
_loggedDataRepos = list()


# ottengo lista contributors della repository in analisi e rispettivi commits (passata come argomento)
def get_repo_contributors(owner, repo):
    if repo in visited_repos:
        return
    # Timer di attesa t per richiesta API github
    time.sleep(t)
    response = requests.get(CONTRIBUTORS_ENDPOINT.format(owner, repo), auth=('socialNetworkAnalysis', 'XTfLGSS3'))
    # manage 204 HTTP response returning None value
    if response.status_code == 204:
        return
    data_json = response.json()
    # TODO rimuovi qui
    _loggedDataContributors.append(data_json)

    visited_repos.add(repo)
    return get_first_five_contributors(data_json)


def get_first_five_contributors(repo_contributors):
    user_list = list()
    if len(repo_contributors) > 5:
        for i in range(len(repo_contributors) - 5, len(repo_contributors)):
            user_list.append(get_contributor_info(repo_contributors[i]))
    else:
        for elem in repo_contributors:
            user_list.append(get_contributor_info(elem))
    return user_list


def get_contributor_info(contributor_dic: Dict):
    return contributor_dic["author"]["login"], contributor_dic["total"]


# ottengo nome_repo, lang_repo
def get_user_repos(user):
    # Timer di attesa t per richiesta API github
    time.sleep(t)
    response = requests.get(REPOS_ENDPOINT.format(user), auth=('socialNetworkAnalysis', 'XTfLGSS3'))
    print(response)
    repos_json = response.json()

    # TODO RIMUOVI QUI
    _loggedDataRepos.append(repos_json)
    repo_list = list()

    for elem in repos_json:
        repo_list.append(get_repos_info(elem))

    return repo_list


def get_repos_info(repos_dic: Dict):
    return repos_dic['name'], repos_dic['language']


# Appends to user_dict five_contributors of the repo repo_name
# It finally enqueues every contributor in a queue and returns this queue
def run_from_data(five_contributors, repo_name, language):
    if five_contributors is None:
        return
    for user in five_contributors:
        username = user[0]
        # The method setdefault() is similar to get(), but will set dict[key]=default if key is not already in dict.
        repos = user_dict.setdefault(username, [])
        repos.append(Repo(repo_name, user[1], language))

        # user repos will be downloaded from the queue
        queue.append(username)
        return queue


def save_data(data, file):
    json.dump(data, open(file, "w"), cls=CustomJsonEncoder)


# For every user u in the queue, it saves u's contributors
def save_user_queue_contributors(user_queue):
    while len(user_queue) > 0:
        user = user_queue.popleft()
        print("Analyzing user: {}".format(user))
        collect_data_on_user_repos(user)


def collect_data_on_user_repos(user):
    # per l'utente in analisi, ottengo lista delle sue repository
    repos_data = get_user_repos(user)
    for repo in repos_data:
        print("Analyzing repo: {}".format(repo[0]))
        # per la repo in analisi, ottengo lista contributors
        repo_contributors = get_repo_contributors(user, repo[0])

        # chiamo funzione run_from_data che inserisce utenti/oggetti Repo in user_dict
        run_from_data(get_first_five_contributors(repo_contributors), repo[0], repo[1])


# funzione di test per analisi errori su specifici user/nodi
# def analyze_specific_user(user):
#     repos_data = get_user_repos(user)
#     for repo in repos_data:
#         contributors_data = get_repo_contributors(user, repo[0])
#         run_from_data(contributors_data, repo[0], repo[1])


def init_crawler():
    repo_contributors = get_repo_contributors("torvalds", "linux",)
    return get_first_five_contributors(repo_contributors)


def main():
    init_five_contributors = init_crawler()
    user_queue = run_from_data(init_five_contributors, "linux", "C")

    save_user_queue_contributors(user_queue)
    save_user_queue_contributors(user_queue)
    save_data(user_dict, "depth2.json")


main()

