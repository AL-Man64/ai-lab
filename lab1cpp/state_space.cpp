#include "state_space.hpp"
#include <fstream>
#include <iostream>
#include <optional>
#include <sstream>
#include <stdexcept>
#include <string>
#include <tuple>
#include <vector>

// Sources:
// * https://stackoverflow.com/a/10058725

// scary function - hope to not touch again
StateSpace StateSpace::parse(const std::string &file_name) {
  if (file_name == "3x3_puzzle.txt") {
    throw std::runtime_error("I give up on parsing this one");
  }

  auto name_map = std::vector<std::string>();
  std::string initial_state_string;
  std::vector<std::string> final_states_string;

  int line_number = 0;
  std::fstream lines(file_name);
  std::string line;

  std::vector<std::string> right_hand_sides;

  while (std::getline(lines, line, '\n')) {
    if (line.empty() || line.front() == '#') {
      continue;
    }

    if (line_number == 0) {
      initial_state_string = line;
      line_number++;
      continue;
    }

    if (line_number == 1) {
      std::stringstream states(line);
      std::string state;

      while (std::getline(states, state, ' ')) {
        final_states_string.push_back(state);
      }

      line_number++;
      continue;
    }

    std::stringstream line_stream(line);
    std::string lhs; // left hand side
    std::string rhs; // right hand side

    std::getline(line_stream, lhs, ':');
    std::getline(line_stream, rhs, ':');

    // Safe(?) to index both of these with the same integer
    name_map.push_back(lhs);
    right_hand_sides.push_back(rhs);
  }

  std::vector<std::vector<std::optional<int>>> transition_table(
      name_map.size());
  for (int i = 0; i < transition_table.size(); i++) {
    transition_table[i] = std::vector<std::optional<int>>(name_map.size());

    std::stringstream next_states(right_hand_sides[i]);
    std::string next_state;

    while (std::getline(next_states, next_state, ' ')) {
      if (next_state.empty()) {
        continue;
      }

      std::stringstream state_cost_pair(next_state);
      std::string state;
      std::string cost;

      std::getline(state_cost_pair, state, ',');
      std::getline(state_cost_pair, cost, ',');

      std::optional<int> index = find_index_of_name(name_map, state);
      if (!index.has_value()) {
        throw std::runtime_error(
            "Unrecoverable error while parsing data: State does not exist");
      }

      int j = index.value();
      transition_table[i][j] = std::stoi(cost);
    }
  }

  std::optional<int> index = find_index_of_name(name_map, initial_state_string);
  if (!index.has_value()) {
    throw std::runtime_error(
        "Unrecoverable error while parsing data: State does not exist");
  }
  int initial_state = index.value();

  std::vector<int> final_states;
  for (const auto &state : final_states_string) {
    std::optional<int> index = find_index_of_name(name_map, state);
    if (!index.has_value()) {
      throw std::runtime_error(
          "Unrecoverable error while parsing data: State does not exist");
    }
    final_states.push_back(index.value());
  }

  std::optional<std::string> heuristic_descriptor_file; // no value yet

  return StateSpace(name_map, transition_table, initial_state, final_states,
                    heuristic_descriptor_file);
}

/* state, cost */
std::vector<std::tuple<int, int>> StateSpace::succ(const int &state) const {
  std::vector<std::tuple<int, int>> successor_states;
  int i = 0;
  for (const std::optional<int> &cost : transition_table[state]) {
    if (cost.has_value()) {
      successor_states.push_back(std::make_tuple(i, cost.value()));
    }
    i += 1;
  }
  return successor_states;
}

std::optional<int>
StateSpace::find_index_of_name(const std::vector<std::string> &names,
                               const std::string &name) {
  std::optional<int> index;

  int i = 0;
  for (auto element : names) {
    if (element == name) {
      index = i;
      break;
    }
    i += 1;
  }

  return index;
}

bool StateSpace::is_goal(const int &state) const {
  bool is_goal;

  int i = 0;
  for (auto element : this->final_states) {
    if (element == state) {
      is_goal = true;
      break;
    }
    i += 1;
  }

  return is_goal;
}

void StateSpace::parse_heuristic(const std::string &heuristic_descriptor_file) {
  this->heuristic_descriptor_file = heuristic_descriptor_file;
  this->heuristic = std::vector<int>(state_names.size());

  std::fstream lines(heuristic_descriptor_file);
  std::string line;

  while (std::getline(lines, line, '\n')) {
    if (line.empty() || line.front() == '#') {
      continue;
    }

    std::stringstream fragments(line);
    std::string name;
    std::string heuristic;

    do {
      std::getline(fragments, name, ':');
    } while (name.empty());
    do {
      std::getline(fragments, heuristic, ':');
    } while (heuristic.empty());

    if (name.empty() || heuristic.empty()) {
      continue;
    }

    std::optional<int> index = find_index_of_name(this->state_names, name);
    if (!index.has_value()) {
      throw std::runtime_error(
          "Unrecoverable error while parsing data: State does not exist");
    }

    this->heuristic[index.value()] = std::stoi(heuristic);
  }
}

std::ostream &operator<<(std::ostream &s, const StateSpace &data) {
  bool first;
  /* begin */
  s << "{ ";

  /* state_names */
  s << "state_names: { ";
  first = true;
  for (auto state : data.state_names) {
    if (first) {
      first = false;
    } else {
      s << ", ";
    }
    s << "\"" << state << "\"";
  }
  s << " }";

  /* transition_table */
  s << ", transition_table: { ";
  first = true;
  for (auto row : data.transition_table) {
    if (first) {
      first = false;
    } else {
      s << ", ";
    }
    s << "{ ";
    bool first = true;
    for (auto element : row) {
      if (first) {
        first = false;
      } else {
        s << ", ";
      }
      if (element.has_value()) {
        s << element.value();
      } else {
        s << "";
      }
    }
    s << " }";
  }
  s << " }";

  /* initial_state */
  s << ", initial_state: " << data.initial_state;

  /* final_states */
  s << ", final_states: { ";
  first = true;
  for (auto state : data.final_states) {
    if (first) {
      first = false;
    } else {
      s << ", ";
    }
    s << state;
  }
  s << " }";

  /* heuristic */
  if (data.heuristic.size() != 0) {
    s << ", heuristic: { ";
    first = true;
    int i = 0;
    for (auto value : data.heuristic) {
      if (first) {
        first = false;
      } else {
        s << ", ";
      }
      s << value;
    }
    s << " }";
  }

  /* end */
  s << " }";

  return s;
}
