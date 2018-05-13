import json

data = json.load(open("data2135.json", "r"))

for user, repo_list in data.items():
    visited_repo = list()
    for repo in repo_list:
        if repo in visited_repo:
            print("MA CHE CAZZ", repo)
            quit()
        visited_repo.append(repo)
