#pragma once
// Algorithms

#include "state_space.hpp"
#include <optional>
#include <string>
#include <vector>

struct Result {
  std::string algorithm;
  std::optional<int> solution;
  unsigned long visited;
  std::vector<int> path;
};

Result bfs(const StateSpace &data);
Result ucs(const StateSpace &data);
Result a_star(const StateSpace &data);
