from json import JSONEncoder, JSONDecoder
from json.decoder import WHITESPACE


class Repo:
    __slots__ = ["name", "commits", "language"]

    def __init__(self, name: str, commits: int, language: str):
        self.name = name
        self.commits = commits
        self.language = language


class CustomJsonEncoder(JSONEncoder):
    """
    Custom encoder che trasforma gli oggetti di tipo Repo in un oggetto json del tipo
    '{"nome_repo": {"commits": n, "language": "l"}}'

    Utilizzo: import json; json.dumps(data, cls=CustomJsonEncoder)
    """

    def __init__(self, *args, skipkeys=False, ensure_ascii=True,
                 check_circular=True, allow_nan=True, sort_keys=False,
                 indent=None, separators=None, default=None):
        super(CustomJsonEncoder, self).__init__(*args, skipkeys, ensure_ascii,
                                                check_circular, allow_nan, sort_keys,
                                                indent, separators, default)

    def default(self, o):
        if type(o) == Repo:
            return {o.name: {"commits": o.commits, "language": o.language}}
        else:
            return o


class CustomJsonDecoder(JSONDecoder):

    def __init__(self, *, object_hook=None, parse_float=None,
                 parse_int=None, parse_constant=None, strict=True,
                 object_pairs_hook=None):
        super(CustomJsonDecoder, self).__init__(object_hook, parse_float, parse_int, parse_constant, strict,
                                                object_pairs_hook)

    def decode(self, s, _w=WHITESPACE.match):
        # TODO DA IMPLEMENTARE, NON OBBLIGATORIAMENTE
        pass