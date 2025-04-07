"""
State space search algorithms
"""

from collections import deque


def parse_input_file(f):
    states = []
    initial_state = None
    goal_states = None
    state_space = {}

    for line in f:
        line = line.strip()
        if line.startswith("#"):
            continue

        if not initial_state:
            initial_state = line
            continue

        if not goal_states:
            goal_states = line.split(" ")
            continue

        split = line.split(":")

        state = split[0]

        # print(f"adding {state} to states", file=sys.stderr)

        states.append(state)
        state_space[len(states) - 1] = []

        if not split[1].strip():
            continue

        for next in split[1].strip().split(" "):
            split = next.split(",")

            next_state = split[0]
            cost = int(split[1])

            state_space[len(states) - 1].append((next_state, cost))

    for k in state_space:
        state_space[k] = [(states.index(state), cost) for state, cost in state_space[k]]

    initial_state = states.index(initial_state)
    goal_states = [states.index(s) for s in goal_states]

    return (states, initial_state, goal_states, state_space)


def parse_heuristic_file(f, states):
    heuristic = [0] * len(states)

    for line in f:
        line = line.strip()
        h = line.split(": ")

        heuristic[states.index(h[0])] = int(h[1])

    return heuristic


def breadth_first_search(initial_state, goal_states, state_space, states):
    result = {
        "solution": None,
        "states_visited": 0,
        "path_length": None,
        "total_cost": None,
        "path": None,
    }

    open = deque([initial_state])
    closed = []

    depths = [None] * len(states)
    depths[initial_state] = 1

    parents = [None] * len(states)

    while open:
        n = open.popleft()
        closed.append(n)

        result["states_visited"] += 1

        if n in goal_states:
            result["solution"] = n
            break

        for m, _ in state_space[n]:
            if m not in open and m not in closed:
                open.append(m)
                depths[m] = depths[n] + 1
                parents[m] = n

    if result["solution"]:
        result["total_cost"] = 0.0
        result["path"] = deque([result["solution"]])

        n = result["solution"]
        while n is not None and n != initial_state:
            result["path"].appendleft(parents[n])

            for t in state_space[parents[n]]:
                if t[0] == n:
                    result["total_cost"] += t[1]

            n = parents[n]

        result["path_length"] = len(result["path"])

    return result


def uniform_cost_search(initial_state, goal_states, state_space, states):
    result = {
        "solution": None,
        "states_visited": 0,
        "path_length": None,
        "total_cost": None,
        "path": None,
    }

    open = [initial_state]
    closed = []

    depths = [None] * len(states)
    depths[initial_state] = 1

    costs = [float("inf")] * len(states)
    costs[initial_state] = 0.0

    parents = [None] * len(states)

    while open:
        open = sorted(open, key=lambda x: costs[x])

        n = open[0]
        open = open[1:]

        closed.append(n)

        result["states_visited"] += 1

        if n in goal_states:
            result["solution"] = n
            break

        for m, c in state_space[n]:
            new_cost = costs[n] + c

            if m not in open and m not in closed:
                open.append(m)
                costs[m] = new_cost
                depths[m] = depths[n] + 1
                parents[m] = n

            elif new_cost < costs[m]:
                if m in closed:
                    closed = [x for x in closed if x != m]
                    open.append(m)

                costs[m] = new_cost
                depths[m] = depths[n] + 1
                parents[m] = n

    if result["solution"]:
        result["total_cost"] = 0.0
        result["path"] = deque([result["solution"]])

        n = result["solution"]
        while n is not None and n != initial_state:
            result["path"].appendleft(parents[n])

            for t in state_space[parents[n]]:
                if t[0] == n:
                    result["total_cost"] += t[1]

            n = parents[n]

        result["path_length"] = len(result["path"])

    return result


def a_star_search(initial_state, goal_states, state_space, states, heuristic):
    result = {
        "solution": None,
        "states_visited": 0,
        "path_length": None,
        "total_cost": None,
        "path": None,
    }

    open = [initial_state]
    closed = []

    depths = [None] * len(states)
    depths[initial_state] = 1

    costs = [float("inf")] * len(states)
    costs[initial_state] = 0.0

    parents = [None] * len(states)

    while open:
        open = sorted(open, key=lambda x: costs[x] + heuristic[x])

        n = open[0]
        open = open[1:]

        closed.append(n)

        result["states_visited"] += 1

        if n in goal_states:
            result["solution"] = n
            break

        for m, c in state_space[n]:
            new_cost = costs[n] + c

            if m not in open and m not in closed:
                open.append(m)
                costs[m] = new_cost
                depths[m] = depths[n] + 1
                parents[m] = n

            elif new_cost < costs[m]:
                if m in closed:
                    closed = [x for x in closed if x != m]
                    open.append(m)

                costs[m] = new_cost
                depths[m] = depths[n] + 1
                parents[m] = n

    if result["solution"]:
        result["total_cost"] = 0.0
        result["path"] = deque([result["solution"]])

        n = result["solution"]
        while n is not None and n != initial_state:
            result["path"].appendleft(parents[n])

            for t in state_space[parents[n]]:
                if t[0] == n:
                    result["total_cost"] += t[1]

            n = parents[n]

        result["path_length"] = len(result["path"])

    return result


def check_optimistic(goal_states, states, state_space, heuristic):
    costs = [float("inf")] * len(states)
    for s in goal_states:
        costs[s] = 0.0

    open = [s for s in goal_states]
    closed = []

    while open:
        open = sorted(open, key=lambda x: costs[x])

        n = open[0]
        open = open[1:]

        closed.append(n)

        for m, c in state_space[n]:
            new_cost = costs[n] + c

            if m not in open and m not in closed:
                open.append(m)
                costs[m] = new_cost

            elif new_cost < costs[m]:
                if m in closed:
                    closed = [x for x in closed if x != m]
                    open.append(m)

                costs[m] = new_cost

    optimistic = True

    for state in range(len(states)):
        if heuristic[state] <= costs[state]:
            print(
                f"[CONDITION]: [OK] h({states[state]}) <= h*: {heuristic[state]:.1f} <= {costs[state]:.1f}"
            )
        else:
            print(
                f"[CONDITION]: [ERR] h({states[state]}) <= h*: {heuristic[state]:.1f} <= {costs[state]:.1f}"
            )
            optimistic = False

    if optimistic:
        print("[CONCLUSION]: Heuristic is optimistic.")
    else:
        print("[CONCLUSION]: Heuristic is not optimistic.")


def check_consistent(state_space, states, heuristic):
    consistent = True

    for state in range(len(states)):
        for transition in state_space[state]:
            (new_state, cost) = transition

            if heuristic[state] <= heuristic[new_state] + cost:
                print(
                    f"[CONDITION]: [OK] h({states[state]}) <= h({states[new_state]}) + c: {heuristic[state]:.1f} <= {heuristic[new_state]:.1f} + {cost:.1f}"
                )
            else:
                # We've found an exception to the rule: the heuristic is not consistent
                consistent = False
                print(
                    f"[CONDITION]: [ERR] h({states[state]}) <= h({states[new_state]}) + c: {heuristic[state]:.1f} <= {heuristic[new_state]:.1f} + {cost:.1f}"
                )

    if consistent:
        print("[CONCLUSION]: Heuristic is consistent.")
    else:
        print("[CONCLUSION]: Heuristic is not consistent.")
