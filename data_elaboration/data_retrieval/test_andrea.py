from typing import List, Dict


class Repo:
    __slots__ = ["name", "commits"]

    def __init__(self, name: str, commits: int):
        self.name = name
        self.commits = commits


class User:
    __slots__ = ["name", "repos"]

    def __init__(self, name: str, repos: List[Repo]):
        self,name = name
        self.repos = repos


gianni = Repo("repotest", 25)

print(gianni.name)


