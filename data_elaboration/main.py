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
    lista: List[User] = []
    for i in range(0, 150000):
        repo_list = []
        for j in range(0, 100):
            repo_list.append(Repo("stocazzo", 420))
        lista.append(User("stograndissimocazzo", repo_list))
    return lista

def create_roba_dic():
    lista: List[Dict] = []
    for i in range(0, 150000):
        repo_list = []
        for j in range(0, 100):
            repo_list.append({"name": "stocazzo", "commits": 420})
        lista.append({"name": "stogasaodcj", "repo": repo_list})
    return lista


def printamilaroba_classi(roba):
    for elem in roba:
        print(elem.name)
        print(elem.repos[0].name)

def printaasdf(roba):
    for elem in roba:
        print(elem['name'])
        print(elem['repo'][0]['name'])



if __name__ == "__main__":
    roba = create_roba_dic()
    printaasdf(roba)
