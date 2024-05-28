#!/usr/bin/env python3


from argparse import ArgumentParser
from csv import DictReader
from math import log2

def read_dataset(path: str) -> list[dict[str, str]]:
    rows = []

    with open(path) as f:
        csv_reader = DictReader(f)
        for row in csv_reader:
            rows.append(row)

    return rows


def build_decision_tree(rows: list[dict[str, str]], depth: int | None = None) -> dict:
    tree: dict[str, str | dict] = {}

    if depth is not None:
        depth -= 1

    # decision name
    dn = ""
    for k in rows[0]:
        dn = k

    total: int = 0
    decisions: dict[str, int] = {}

    if all([x[dn] == rows[0][dn] for x in rows]):
        tree["decision"] = rows[0][dn]
        return tree

    for row in rows:
        if row[dn] not in decisions:
            decisions[row[dn]] = 0

        total += 1
        decisions[row[dn]] += 1

    if depth is not None and depth <= 0:
        max_val = 0
        for v in decisions.values():
            if v > max_val:
                max_val = v

        most_frequent = [x for x in decisions if decisions[x] == max_val]
        most_frequent.sort()

        tree["decision"] = most_frequent[0]
        return tree

    initial_entropy: float = 0

    for decision in decisions.values():
        probability: float = decision / total
        initial_entropy -= probability * log2(probability)

    ig: float = 0.0
    igf: str = ""

    for feature in [x for x in rows[0] if x != dn]:
        ig_local: float = initial_entropy

        for value in {x[feature] for x in rows if feature in x}:
            total_val: int = 0
            for k in decisions:
                decisions[k] = 0

            for row in [x for x in rows if x[feature] == value]:
                total_val += 1
                decisions[row[dn]] += 1

            entropy: float = 0

            for decision in decisions.values():
                probability: float = decision / total_val

                if probability != 0.0:
                    entropy -= probability * log2(probability)
                else:
                    entropy = 0.0

            ig_local -= entropy * total_val / total

        print(f"IG({feature})={ig_local:.4f}  ", end="")

        if ig_local > ig:
            ig = ig_local
            igf = feature

    print()

    tree["feature"] = igf
    for value in {x[igf] for x in rows if igf in x}:
        new_dataset: list[dict[str, str]] = []
        for x in rows:
            if x[igf] == value and {k: x[k] for k in x if k != igf} not in new_dataset:
                new_dataset.append({k: x[k] for k in x if k != igf})

        tree[value] = build_decision_tree(
            [{k: x[k] for k in x if k != igf} for x in rows if x[igf] == value], depth
        )

    return tree


def print_branches(tree: dict, prev: str = "", iteration: int = 1) -> None:
    if iteration == 1:
        print("[BRANCHES]:")

    if "decision" not in tree:
        for branch in {k: tree[k] for k in tree if k != "feature"}:
            print_branches(
                tree[branch],
                prev + f"{iteration}:{tree['feature']}={branch} ",
                iteration + 1,
            )

    else:
        print(f"{prev}{tree['decision']}")


def predict(tree: dict, data: dict[str, str], dataset: list[dict[str, str]]) -> tuple:
    # decision name
    dn = ""
    for k in data:
        dn = k

    if "decision" in tree:
        prediction = tree["decision"]
    else:
        if data[tree["feature"]] not in tree:
            decisions: dict[str, int] = {}

            for row in dataset:
                if row[dn] not in decisions:
                    decisions[row[dn]] = 0

                decisions[row[dn]] += 1

            max_val = 0
            for v in decisions.values():
                max_val = v

            most_frequent = [x for x in decisions if decisions[x] == max_val]
            most_frequent.sort()

            prediction = most_frequent[0]

        else:
            prediction, _ = predict(tree[data[tree["feature"]]], data, dataset)

    return prediction, data[dn]


def print_predictions_and_accuracy(tree, test_dataset, dataset) -> None:
    total: int = 0
    accurate: int = 0

    print("[PREDICTIONS]: ", end="")
    for row in test_dataset:
        prediction, expected = predict(tree, row, dataset)
        print(prediction, end=" ")

        if prediction == expected:
            accurate += 1

        total += 1

    accuracy: float = accurate / total

    print()
    print(f"[ACCURACY]: {accuracy:.5f}")


def print_confusion_matrix(tree, test_dataset, dataset) -> None:
    confusion_matrix: list[list[int]] = []

    # decision name
    dn = ""
    for k in test_dataset[0]:
        dn = k

    decisions: list[str] = []

    for row in test_dataset:
        if row[dn] not in decisions:
            decisions.append(row[dn])
            if len(confusion_matrix) > 0:
                confusion_matrix.append([0 for _ in confusion_matrix[0]])
            else:
                confusion_matrix.append([])
            for row in confusion_matrix:
                row.append(0)

    decisions.sort()

    for row in test_dataset:
        prediction, expected = predict(tree, row, dataset)

        ei = decisions.index(expected)
        pi = decisions.index(prediction)

        confusion_matrix[ei][pi] += 1

    print("[CONFUSION_MATRIX]:")

    for row in confusion_matrix:
        for val in row:
            print(val, end=" ")

        print()


def main() -> None:
    ap = ArgumentParser()

    ap.add_argument(
        "dataset",
        type=str,
        help="path of the dataset file for the model to be trained on",
    )
    ap.add_argument(
        "test_dataset",
        type=str,
        help="path of the dataset file for the model to be tested on",
    )

    ap.add_argument(
        "depth",
        type=int,
        nargs="?",
        default=None,
        help="depth for the decision tree to be built",
    )

    args = ap.parse_args()

    dataset: list[dict[str, str]] = read_dataset(args.dataset)
    test_dataset: list[dict[str, str]] = read_dataset(args.test_dataset)

    decision_tree = build_decision_tree(
        dataset, args.depth + 1 if args.depth is not None else None
    )

    print_branches(decision_tree)
    print_predictions_and_accuracy(decision_tree, test_dataset, dataset)
    print_confusion_matrix(decision_tree, test_dataset, dataset)


if __name__ == "__main__":
    main()
