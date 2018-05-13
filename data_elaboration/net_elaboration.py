import json


def associate_users_to_repos():
    repo_dict = dict()
    data = json.load(open("./data.json"))
    for user, repo in data.items():
        for r in repo:
            for reponame, val in r.items():
                a = repo_dict.setdefault(reponame, [])
                a.append((user, val["commits"], val["language"]))
    return repo_dict


def print_data(repo_dict):
    for reponame, users in repo_dict.items():
        print("\n###################################################################")
        print("Hanno collaborato a ", reponame, " (linguaggio ", users[0][2], "):\n")
        for user in users:
            print(user[0], "con ", user[1], "commits")


def print_collab_data(collab_data):
    for user, collaborators in collab_data.items():
        print("\n" + user, "ha collaborato con i seguenti utenti:\n")
        for collab in collaborators:
            print(collab)
        print("####################################################\n")


def get_collaboration_data(repo_dict):
    collaboration_dict = dict()
    for repo_name, users in repo_dict.items():
        for user in users:
            user_collaborators = collaboration_dict.setdefault(user[0], set())
            _users = users.copy()
            _users.remove(user)
            for u in _users:
                user_collaborators.add(u[0])
    return collaboration_dict


repo_dict = associate_users_to_repos()

collaboration_data = get_collaboration_data(repo_dict)
print_collab_data(collaboration_data)
