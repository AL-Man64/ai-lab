#include "algos.hpp"
#include "state_space.hpp"
#include <algorithm>
#include <iostream>
#include <iterator>
#include <list>
#include <optional>
#include <set>
#include <stdexcept>

// Sources
// * https://stackoverflow.com/a/16747600

/* function breadthFirstSearch(s0, succ, goal) */
Result bfs(const StateSpace &data) {
  /* -> Complete obtained output: */
  /* # BFS */
  /* [FOUND_SOLUTION]: yes */
  /* [STATES_VISITED]: 15 */
  /* [PATH_LENGTH]: 8 */
  /* [TOTAL_COST]: 77 */
  /* [PATH]: A => F => D => C => B => I => E => O */
  /* -> Complete expected output: */
  /* # BFS */
  /* [FOUND_SOLUTION]: yes */
  /* [STATES_VISITED]: 15 */
  /* [PATH_LENGTH]: 5 */
  /* [TOTAL_COST]: 54.0 */
  /* [PATH]: A => D => H => E => O */

  /* open <- [initial(s0)] */
  std::list<int> open = {data.initial_state};
  std::set<int> visited = {};
  std::vector<int> path = {};
  std::vector<std::optional<int>> prev_states(data.transition_table.size());

  /* while open != [] do */
  while (!open.empty()) {
    /* n <- removeHead(open) */
    const int n = open.front();
    visited.insert(n);
    open.pop_front();
    /* if goal(state(n)) then return n */
    if (data.is_goal(n)) {
      path.push_back(n);
      while (path.back() != data.initial_state) {
        path.push_back(prev_states[path.back()].value());
      }
      std::reverse(path.begin(), path.end());
      return Result{.algorithm = "BFS",
                    .solution = n,
                    .visited = visited.size(),
                    .path = path};
    }
    /* for m in expand(n, succ) do */
    for (const auto &m : data.succ(n)) {
      /* insertBack(m, open) */
      if (visited.find(std::get<0>(m)) == visited.end()) {
        std::cout << (std::distance(visited.find(std::get<0>(m)),
                                    visited.end()))
                  << '\n';
        std::cout << "Expanding " << data.state_names[n] << " into "
                  << data.state_names[std::get<0>(m)] << '\n';
        open.push_back(std::get<0>(m));
        prev_states[std::get<0>(m)] = n;
      }
    }
  }
  /* return fail */
  return Result{.algorithm = "BFS", .visited = visited.size()};
}

/* function uniformCostSearch(s0, succ, goal) */
Result ucs(const StateSpace &data) {
  /* open <- [initial(s0)] */
  std::list<int> open = {data.initial_state};
  std::set<int> visited = {};
  std::vector<int> path = {};
  std::vector<std::optional<int>> prev_states(data.transition_table.size());
  /* while open != [] do */
  while (!open.empty()) {
    /* n <- removeHead(open) */
    const int n = open.front();
    visited.insert(n);
    open.pop_front();
    /* if goal(state(n)) then return n */
    if (data.is_goal(n)) {
      path.push_back(n);
      while (path.back() != data.initial_state) {
        path.push_back(prev_states[path.back()].value());
      }
      std::reverse(path.begin(), path.end());
      return Result{.algorithm = "UCS",
                    .solution = n,
                    .visited = visited.size(),
                    .path = path};
    }
    /* for m in expand(n, succ) do */
    for (const auto &m : data.succ(n)) {
      /* insertSortedBy(g, m, open) */
      if (visited.find(std::get<0>(m)) == visited.end()) {
        int i = 0;
        for (const auto &e : open) {
          if (std::get<0>(m) > e) {
            break;
          }
        }
        auto l_front = open.begin();
        std::advance(l_front, i);
        open.insert(l_front, std::get<0>(m));
        prev_states[std::get<0>(m)] = n;
      }
    }
  }
  /* return fail */
  return Result{.algorithm = "UCS", .visited = visited.size()};
}

/* function search(s0, succ, goal, h) */
Result a_star(const StateSpace &data) {
  if (!data.heuristic_descriptor_file.has_value()) {
    throw std::runtime_error("Error: no heuristic descriptor was passed");
  }
  /* open <- [initial(s0)] */
  std::list<int> open = {data.initial_state};
  /* closed <- empty */
  std::set<int> closed;
  std::vector<int> path = {};
  std::vector<std::optional<int>> prev_states(data.transition_table.size());
  /* while open != [] do */
  while (!open.empty()) {
    std::cerr << "open: { ";
    bool first = true;
    for (const auto &e : open) {
      if (first) {
        first = false;
      } else {
        std::cerr << ", ";
      }
      std::cerr << data.state_names[e];
    }
    std::cerr << " }\n";
    /* n <- removeHead(open) */
    const int n = open.front();
    open.pop_front();
    /* if goal(state(n)) then return n */
    if (data.is_goal(n)) {
      path.push_back(n);
      while (path.back() != data.initial_state) {
        path.push_back(prev_states[path.back()].value());
      }
      std::reverse(path.begin(), path.end());
      return Result{.algorithm = "UCS",
                    .solution = n,
                    .visited = closed.size(),
                    .path = path};
    }
    /* closed <- closed union { n } */
    closed.insert(n);
    /* for m in expand(n) do */
    for (const auto &m : data.succ(n)) {
      // FIX: take into account open states

      /* if exists m' in (closed union open) such that state(m') = state(m) then
       */
      if (closed.find(std::get<0>(m)) != closed.end()) {
        /* if g(m') < g(m) then continue */
        /* else remove(m', closed union open) */
        closed.erase(closed.find(std::get<0>(m)));
      }
      /* insertSortedBy(f, m, open) */
      if (closed.find(std::get<0>(m)) == closed.end()) {
        int i = 0;
        for (const auto &e : open) {
          if (std::get<0>(m) > e) {
            break;
          }
        }
        auto l_front = open.begin();
        std::advance(l_front, i);
        open.insert(l_front, std::get<0>(m));
        prev_states[std::get<0>(m)] = n;
      }
    }
  }
  /* return fail */
  return Result{.algorithm = "A-STAR", .visited = closed.size()};
}
