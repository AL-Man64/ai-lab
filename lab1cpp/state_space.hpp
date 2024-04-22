#pragma once

#include <optional>
#include <ostream>
#include <string>
#include <vector>

class StateSpace {
public:
  static StateSpace parse(const std::string &file_name);
  static std::optional<int>
  find_index_of_name(const std::vector<std::string> &names,
                     const std::string &name);

  StateSpace() {}
  StateSpace(
      const std::vector<std::string> &state_names,
      const std::vector<std::vector<std::optional<int>>> &transition_table,
      const int &initial_state, const std::vector<int> &final_states,
      const std::optional<std::string> &heuristic_descriptor_file)
      : state_names(state_names), transition_table(transition_table),
        initial_state(initial_state), final_states(final_states),
        heuristic_descriptor_file(heuristic_descriptor_file) {}

  std::vector<std::tuple<int, int>> succ(const int &state) const;
  bool is_goal(const int &state) const;
  void parse_heuristic(const std::string &heuristic_descriptor_file);

  std::vector<std::string> state_names;
  std::vector<std::vector<std::optional<int>>> transition_table;
  int initial_state;
  std::vector<int> final_states;
  std::vector<int> heuristic;
  std::optional<std::string> heuristic_descriptor_file;

private:
};

std::ostream &operator<<(std::ostream &s, const StateSpace &data);
