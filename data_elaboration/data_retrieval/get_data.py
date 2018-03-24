from typing import Dict
import requests
import json
import time
from data_elaboration.data_retrieval.data_structures import Repo, CustomJsonEncoder

CONTRIBUTORS_ENDPOINT = "https://api.github.com/repos/{}/{}/stats/contributors"
REPOS_ENDPOINT = "https://api.github.com/users/{}/repos"
user_dict = dict()
visited_repos = set("linux")
# For requests using Basic Authentication or OAuth, you can make up to 5000 requests per hour.
# t_min = 5000/(60*60) = 1.38s
t = 2
depth = 3


# ottengo lista contributors della repository in analisi e rispettivi commits (passata come argomento)
def get_repo_contributors(owner, repo):
    # Timer di attesa t per richiesta API github
    time.sleep(t)
    response = requests.get(CONTRIBUTORS_ENDPOINT.format(owner, repo), auth=('socialNetworkAnalysis', 'XTfLGSS3'))
    print(response)
    # manage 204 HTTP response returning None value
    if response.status_code == 204:
        return
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


def get_contributor_info(contributor_dic: Dict):
    return contributor_dic["author"]["login"], contributor_dic["total"]


# ottengo nome_repo, lang_repo
def get_user_repos(user):
    # Timer di attesa t per richiesta API github
    time.sleep(t)
    response = requests.get(REPOS_ENDPOINT.format(user), auth=('socialNetworkAnalysis', 'XTfLGSS3'))
    print(response)
    repos_json = response.json()
    repo_list = list()

    for elem in repos_json:
        repo_list.append(get_repos_info(elem))

    return repo_list


def get_repos_info(repos_dic: Dict):
    return repos_dic['name'], repos_dic['language']


def run_from_data(data, repo_name, language):
    if data is None:
        return
    for user in data:
        username = user[0]
        # The method setdefault() is similar to get(), but will set dict[key]=default if key is not already in dict.
        repos = user_dict.setdefault(username, [])
        repos.append(Repo(repo_name, user[1], language))


def save_data(data, file):
    json.dump(data, open(file, "w"), cls=CustomJsonEncoder)


def analyze_to_depth(desired_depth):
    for x in range(desired_depth):
        _user_dict_copy = user_dict.copy()
        # individuo in user_dict gli utenti di partenza dell'analisi
        for user in _user_dict_copy:
            print("Analyzing user: {}".format(user))
            # per l'utente in analisi, ottengo lista delle sue repository
            repos_data = get_user_repos(user)
            for repo in repos_data:
                print(repo)
                if repo in visited_repos:
                    continue
                # per la repo in analisi, ottengo lista contributors
                contributors_data = get_repo_contributors(user, repo[0])
                # chiamo funzione run_from_data che inserisce utenti/oggetti Repo in user_dict
                run_from_data(contributors_data, repo[0], repo[1])


# funzione di test per analisi errori su specifici user/nodi
def analyze_specific_user(user):
    repos_data = get_user_repos(user)
    for repo in repos_data:
        # print(repo[0])
        contributors_data = get_repo_contributors(user, repo[0])
        run_from_data(contributors_data, repo[0], repo[1])


def main():
    data = get_repo_contributors("torvalds", "linux",)
    # save_data(data, "salvo_da_funzione.json")
    # data = json.load(open("salvo_da_funzione.json", "r"))

    run_from_data(data, "linux", "C")
    analyze_to_depth(depth)
    save_data(user_dict, "depth3_no_linux.json")


main()

