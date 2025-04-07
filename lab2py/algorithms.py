def _load_list_of_clauses(path_to_list_of_clauses: str) -> list[set[str]]:
    pass


def _clause_is_redundant_or_irrelevant(
    clause: set[str], list_of_clauses: list[set[str]]
):
    pass


def resolution(path_to_list_of_clauses: str):
    list_of_clauses: list[set[str]] = _load_list_of_clauses(path_to_list_of_clauses)
    query = list_of_clauses.pop()

    list_of_clauses = [
        c
        for c in list_of_clauses
        if not _clause_is_redundant_or_irrelevant(c, list_of_clauses)
    ]
