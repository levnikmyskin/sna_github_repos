

class Repo:
    __slots__ = ["name", "commits", "language"]

    def __int__(self, name: str, commits: int, language: str ):
        self.name = name
        self.commits = commits
        self.language = language



