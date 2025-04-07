#!/usr/bin/env python
import cli
import search


def do_search(args, initial_state, goal_states, state_space, states, heuristic):
    result = {}

    if args.alg == "bfs":
        print("# BFS")
        result = search.breadth_first_search(
            initial_state, goal_states, state_space, states
        )
    elif args.alg == "ucs":
        print("# UCS")
        result = search.uniform_cost_search(
            initial_state, goal_states, state_space, states
        )
    elif args.alg == "astar":
        print("# A-STAR")
        result = search.a_star_search(
            initial_state, goal_states, state_space, states, heuristic
        )
    else:
        raise Exception("Unknown algorithm, please enter `bfs`, `ucs` or `astar`")

    print(f"[FOUND_SOLUTION]: {'yes' if result['solution'] else 'no'}")
    print(f"[STATES_VISITED]: {result['states_visited']}")

    if result["path_length"]:
        print("[PATH_LENGTH]:", result["path_length"])

    if result["total_cost"]:
        print(f"[TOTAL_COST]: {result['total_cost']:.1f}")

    if result["path"]:
        print("[PATH]: ", end="")
        for i, node in enumerate(result["path"]):
            if i != 0:
                print(" => ", end="")
            print(states[node], end="")
        print()


def main():
    args = cli.parse_args()

    with open(args.ss, "r") as f:
        states, initial_state, goal_states, state_space = search.parse_input_file(f)

    heuristic = None
    if args.h:
        with open(args.h) as f:
            heuristic = search.parse_heuristic_file(f, states)

    if args.alg:
        do_search(args, initial_state, goal_states, state_space, states, heuristic)
    elif args.check_optimistic:
        search.check_optimistic(goal_states, states, state_space, heuristic)
    elif args.check_consistent:
        search.check_consistent(state_space, states, heuristic)


if __name__ == "__main__":
    main()
