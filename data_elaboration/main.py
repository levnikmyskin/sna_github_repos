from typing import List, Dict
import timeit


class Repo:
    __slots__ = ["name", "commits"]

    def __init__(self, name: str, commits: int):
        self.name = name
        self.commits = commits


class User:
    __slots__ = ["name", "repos"]

    def __init__(self, name: str, repos: List[Repo]):
        self.name = name
        self.repos = repos


def create_roba_classi():
    dick = dict()
    for i in range(0, 150000):
        repo_list = []
        for j in range(0, 100):
            repo_list.append(Repo("stocazzo", 420))
        dick[i] = repo_list
    return dick


def create_roba_dic():
    dick = dict()
    for i in range(0, 150000):
        repo_list = []
        for j in range(0, 100):
            repo_list.append({"name": "stocazzo", "commits": 420})
        dick[i] = repo_list
    return dick


def printamilaroba_classi(roba):
    for i, elem in enumerate(roba):
        print(roba[i])
        print(roba[i][0].name)

def printaasdf(roba):
    for i, elem in enumerate(roba):
        print(roba[i])
        print(roba[i][0]['name'])



if __name__ == "__main__":
    roba = create_roba_classi()
    printamilaroba_classi(roba)
