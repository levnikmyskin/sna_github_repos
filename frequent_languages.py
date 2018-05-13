import json
import collections

d = json.load(open("data2135.json", "r"))

language_list = list()

for _, repo_list in d.items():
    for repo in repo_list:
        for _, repoinfo in repo.items():
            language_list.append(repoinfo["language"])

c = collections.Counter(language_list)
print(c.most_common())

