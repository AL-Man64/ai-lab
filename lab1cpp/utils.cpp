#include "utils.hpp"
#include "algos.hpp"
#include <iostream>

void print_result(const Result &result, const StateSpace &data) {
  std::cout << "# " << result.algorithm;
  if (result.algorithm == "A-STAR") {
    std::cout << " " << data.heuristic_descriptor_file.value();
  }
  std::cout << '\n';
  std::cout << "[FOUND_SOLUTION]: "
            << (result.solution.has_value() ? "yes" : "no") << '\n';
  if (result.solution.has_value()) {
    std::cout << "[STATES_VISITED]: " << result.visited << '\n';
    std::cout << "[PATH_LENGTH]: " << result.path.size() << '\n';
    int cost = 0;
    for (int i = 0; i < result.path.size() - 1; i++) {
      cost += data.transition_table[result.path[i]][result.path[i + 1]].value();
    }
    std::cout << "[TOTAL_COST]: " << cost << '\n';
    std::cout << "[PATH]: ";
    bool first = true;
    for (const auto &state : result.path) {
      if (first) {
        first = false;
      } else {
        std::cout << " => ";
      }
      std::cout << data.state_names[state];
    }
  }
  std::cout << '\n';
}
