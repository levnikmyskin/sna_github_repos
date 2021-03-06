from typing import Dict
import requests
import json
import time
import traceback
from data_elaboration.data_retrieval.data_structures import Repo, CustomJsonEncoder

CONTRIBUTORS_ENDPOINT = "https://api.github.com/repos/{}/{}/stats/contributors"
REPOS_ENDPOINT = "https://api.github.com/users/{}/repos"
queue = list()
visited_repos = set()


# ottengo lista contributors della repository in analisi e rispettivi commits (passata come argomento)
def get_repo_contributors(owner, repo):
    if repo in visited_repos:
        return
    # Timer di attesa per richiesta API github
    time.sleep(0.85)
    response = requests.get(CONTRIBUTORS_ENDPOINT.format(owner, repo), auth=('socialNetworkAnalysis', 'XTfLGSS3'))
    # manage 204 HTTP response returning None value
    if response.status_code != 200:
        return
    repo_contributors = response.json()

    visited_repos.add(repo)
    return repo_contributors


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
    response = requests.get(REPOS_ENDPOINT.format(user), auth=('socialNetworkAnalysis', 'XTfLGSS3'))
    print(response)
    repos_json = response.json()

    repo_list = list()

    for elem in repos_json:
        repo_list.append(get_repos_info(elem))

    return repo_list


def get_repos_info(repos_dic: Dict):
    return repos_dic['name'], repos_dic['language']


# Aggiunge a user_dict i five_contributors della repo repo_name
# Infine mette in una coda ogni contributore e la ritorna
def save_user_and_enqueue_it(five_contributors, repo_name, language, user_dict):
    if five_contributors is None: 
        return
    for user in five_contributors:
        username = user[0]
        # The method setdefault() is similar to get(), but will set dict[key]=default if key is not already in dict.
        repos = user_dict.setdefault(username, [])
        repos.append(Repo(repo_name, user[1], language))

        # user repos will be downloaded from the queue
        queue.append(username)


def save_data(data, file):
    json.dump(data, open(file, "w"), cls=CustomJsonEncoder)
    with open("queue_luglio2.py", "a") as q:
        q.write("queue = ")
        q.write(str(queue))


# Per ogni utente u nella coda, ne salva i contributori
def save_user_queue_contributors(queue, user_dict):
    queue_copy = queue.copy()
    queue.clear()
    for user in queue_copy:
        print("Analyzing user: {}".format(user))
        repos_data = get_user_repos(user)
        collect_data_on_user_repos(user, repos_data, user_dict)


def collect_data_on_user_repos(user, repos_data, user_dict):
    # per l'utente in analisi, ottengo lista delle sue repository
    for repo in repos_data:
        print("Analyzing repo: {}".format(repo[0]))
        # per la repo in analisi, ottengo lista contributors
        repo_contributors = get_repo_contributors(user, repo[0])
        if not repo_contributors:
            continue

        save_user_and_enqueue_it(get_first_five_contributors(repo_contributors), repo[0], repo[1], user_dict)


def init_crawler():
    repo_contributors = get_repo_contributors("torvalds", "linux",)
    return get_first_five_contributors(repo_contributors)


def run_crawler():
    user_dict = dict()
    try:
        init_five_contributors = init_crawler()
        save_user_and_enqueue_it(init_five_contributors, "linux", "C", user_dict)

        save_user_queue_contributors(queue, user_dict)
        save_user_queue_contributors(queue, user_dict)
        save_user_queue_contributors(queue, user_dict)
        save_user_queue_contributors(queue, user_dict)
        save_user_queue_contributors(queue, user_dict)
    except:
        print(traceback.format_exc())
    finally:
        save_data(user_dict, "luglio2.json")
