import requests
import json
from typing import List, Dict
from pprint import pprint



def getData(endpoint):
    response = requests.get(endpoint)
    dataJson = response.json()

    return dataJson


def manageJson(data):
    dictCommitters = {}

    for x in range(len(data) - 5, len(data)):
        dictCommitters[data[x]["author"]["login"]] = data[x]["author"]["repos_url"]

    return dictCommitters


def manageJsonRepo(data):
    dictRepos = {}

    for x in range(len(data)):
        dictRepos[repoData[x]["name"]] = repoData[x]["language"]

    return dictRepos


class Repo:
    __slots__ = ["name", "language"]

    def __init__(self, name: str, language: str):
        self.name = name
        self.language= language


class User:
    __slots__ = ["name", "repos", "user_repos", "commits"]

    def __init__(self, name: str, repos: List[Repo], user_repos: str, commits: int):
        self.name = name
        self.repos = repos
        self.user_repos = user_repos
        self.commits = commits



# PSEUDO-MAIN --------------------------------------------------------------------

# reposUrl = "https://api.github.com/repos/torvalds/linux/stats/contributors"
#
# committersData = getData(reposUrl)

# json.dump(committersData, open("commitersData.json", "w"))
# d = manageJson(committersData)
#
# json.dump(d, open("nuovo.json", "w"))


d = json.load(open("nuovo.json", "r"))

c = json.load(open("commitersData.json", "r"))

e = json.load(open("repoData.json", "r"))

# fisso repo di Partenza e ne creo un oggetto Repo da passare poi ad oggetti Utenti
repo_name = "Linux"
linux = Repo(repo_name, "C++")

listUsers = []

# creo gli oggetti Utenti con la prima lista di Repo imposatata manualmente
# su repo di partenza analisi, dati da CommitersData.json
for i in range(len(c) - 5, len(c)):
    user_name = (c[i]["author"]["login"])
    user_commits = (c[i]["total"])
    user_repos = (c[i]["author"]["repos_url"])
    user_commits = (c[i]["total"])
    listUsers.append(User(user_name, [linux], user_repos, user_commits))

# eseguo chiamata api utilizzando repoUrl = listUsers[x].user_repos, salvo json
visitedUsers = []
# for user in listUsers not in visitedUsers:
for x in range(len(listUsers)):
    repoUrl = listUsers[x].user_repos
    # print(repoUrl)
    # repoData = getData(repoUrl)
    # json.dump(repoData, open("repoData.json", "w"))

# aggiungo agli utenti i rispettivi nuovi oggetti Repo acquisiti da file json repoData
for i in range(len(e)):
    repo_name = (e[i]["name"])
    repo_language = (e[i]["language"])
    test = Repo(repo_name, repo_language)
    listUsers[0].repos.append(test)
    # print(test.name, test.language)

#stampa di controllo

# sull'unico utente aggioranto ehehehe
print(listUsers[0].commits)

for i in range(len(listUsers[0].repos)):
    temp = listUsers[0].repos[i].name
    print(temp)










# for x in range(len(listUsers)):
#     print(listUsers[x].name)
#     print(listUsers[x].user_repos)
#     print(listUsers[x].commits)
#     print(linux.name)
#     print("--------")






# for key, value in d.items():
#     print(key), print(value)
#     repoUrl = value
#     repoData = getData(repoUrl)
#     l = manageJsonRepo(repoData)
#     print(l)



