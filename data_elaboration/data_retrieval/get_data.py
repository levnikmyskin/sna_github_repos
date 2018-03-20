from typing import Dict
import requests
import json
from data_elaboration.data_retrieval.data_structures import Repo


CONTRIBUTORS_ENDPOINT = "https://api.github.com/repos/{}/{}/stats/contributors"
user_dict = dict()
visited_user = list()
depth = 0


def get_contributor_info(contributor_dic: Dict):
    return contributor_dic["author"]["login"], contributor_dic["total"], contributor_dic["author"]["repos_url"]


def get_data(owner, repo):
    response = requests.get(CONTRIBUTORS_ENDPOINT.format(owner, repo))
    data_json = response.json()
    data_list = []

    if len(data_json) > 5:
        for i in range(len(data_json) - 5, len(data_json)):
            data_list.append(get_contributor_info(data_json[i]))
    else:
        for elem in data_json:
            data_list.append(get_contributor_info(elem))
    return data_list


def get_user_repos(repos_url):
    repos = requests.get(repos_url).json()
    if len(user_dict) < 5:
        for repo in repos:
            main(repo['owner']['login'], repo['name'])


def run_from_data(data, repo_name):
    for user in data:
        if depth > 3:
            continue
        username = user[0]
        repos = user_dict.setdefault(username, [])
        repos.append(Repo(repo_name, user[1]))
        get_user_repos(user[2])


def main(owner, repo):
    data = get_data(owner, repo)
    run_from_data(data, repo)


main("torvalds", "linux")

