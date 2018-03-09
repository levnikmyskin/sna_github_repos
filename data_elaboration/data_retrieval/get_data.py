import requests
import json


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


# PSEUDO-MAIN --------------------------------------------------------------------

# reposUrl = "https://api.github.com/repos/torvalds/linux/stats/contributors"
#
# committersData = getData(reposUrl)
#
# d = manageJson(committersData)
#
# json.dump(d, open("nuovo.json", "w"))

d = json.load(open("nuovo.json", "r"))

for key, value in d.items():
    print(key), print(value)
    repoUrl = value
    repoData = getData(repoUrl)
    l = manageJsonRepo(repoData)
    print(l)



