import argparse

_parser = argparse.ArgumentParser()

_parser.add_argument(
    "--alg",
    type=str,
    help="kratica za algoritam za pretrazivanje (vrijednosti: bfs, ucs, ili astar)",
)
_parser.add_argument(
    "--ss", required=True, type=str, help="putanja do opisnika prostora stanja"
)
_parser.add_argument("--h", type=str, help="putanja do opisnika heuristike")
_parser.add_argument(
    "--check-optimistic",
    help="zastavica koja signalizira da se za danu heuristiku zeli provjeriti optimisticnost",
    action="store_true",
)
_parser.add_argument(
    "--check-consistent",
    help="zastavica koja signalizira da se za danu heuristiku zeli provjeriti konsistentnost",
    action="store_true",
)


def parse_args():
    return _parser.parse_args()
