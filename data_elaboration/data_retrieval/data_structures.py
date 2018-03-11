

class Repo:
    __slots__ = ["name", "commits"]

    def __init__(self, name: str, commits: int):
        self.name = name
        self.commits = commits
