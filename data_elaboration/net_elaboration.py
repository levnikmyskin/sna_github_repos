import json
import csv
import networkx as nx


def get_user_language_dict(json_file):
    user_dict = dict()
    for user, repo in json_file.items():
        lang_dict = dict()
        for r in repo:
            for reponame, val in r.items():
                lang = lang_dict.setdefault(val["language"], 0)
                lang_dict[val["language"]] = lang + val["commits"]
        lang_dict = sorted(lang_dict.items(), key=lambda t: t[1], reverse=True)

        user_dict[user] = lang_dict[0]
    return user_dict


def associate_users_to_repos(json_file, user_lang_dict):
    repo_dic = dict()
    for user, repos in json_file.items():
        for r in repos:
            for reponame, val in r.items():
                a = repo_dic.setdefault(reponame, [])
                a.append((user, val["commits"], user_lang_dict[user][0]))
    return repo_dic


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


def elaborate_and_save_csvEDGES_for_gephi(repo_dict):
    with open('network.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for repo_name, users in repo_dict.items():
            for user in users:
                _users = users.copy()
                _users.remove(user)
                for u in _users:
                    lang = u[2] if u[2] is not None else "null"
                    writer.writerow([user[0], u[0], u[1], lang])

# TODO: Capire se questa funzione serve? Su gephi possiamo importare direttamente edgelist (come su nx)...
def elaborate_and_save_csvNODES_for_gephi(user_dict):
    with open('networkNODES.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for user, lang in user_dict.items():
            writer.writerow([[user][0], [user][0], lang[0]])


def elaborate_and_save_edgelist(repo_dict):
    with open('edgelist.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for repo_name, users in repo_dict.items():
            for user in users:
                _users = users.copy()
                _users.remove(user)
                for u in _users:
                    lang = u[2] if u[2] is not None else "null"
                    writer.writerow([user[0], u[0], u[1], lang])


def get_json_to_csv(json_file):
    data = json.load(open(json_file, "r"))
    user_language_dict = get_user_language_dict(data)
    repo_dict = associate_users_to_repos(data, user_language_dict)
    elaborate_and_save_edgelist(repo_dict)
    # elaborate_csvEDGES_for_gephi(repo_dict)
    # elaborate_csvNODES_for_gephi(user_language_dict)

