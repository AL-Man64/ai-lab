#include "algos.hpp"
#include "args.hpp"
#include "state_space.hpp"
#include "utils.hpp"
#include <cstdlib>
#include <iostream>
#include <stdexcept>
#include <string>

const std::string ISTRA_TXT = R"(#
Pula
Buzet
Baderna: Višnjan,13 Poreč,14 Pazin,19 Kanfanar,19
Barban: Pula,28 Labin,15
Buje: Umag,13 Grožnjan,8
Buzet: Lupoglav,15 Motovun,18
Grožnjan: Buje,8 Motovun,15 Višnjan,19
Kanfanar: Baderna,19 Rovinj,18 Žminj,6 Vodnjan,29
Labin: Barban,15 Lupoglav,42
Lupoglav: Labin,42 Opatija,29 Pazin,23 Buzet,15
Medulin: Pula,9
Motovun: Buzet,18 Grožnjan,15 Pazin,20
Opatija: Lupoglav,29
Pazin: Baderna,19 Motovun,20 Žminj,17 Lupoglav,23
Poreč: Baderna,14
Pula: Vodnjan,12 Barban,28 Medulin,9
Rovinj: Kanfanar,18
Umag: Buje,13
Višnjan: Grožnjan,19 Baderna,13
Vodnjan: Kanfanar,29 Pula,12
Žminj: Kanfanar,6 Pazin,17
)";

const std::string ISTRA_HEURISTIC_TXT = R"(Baderna: 25
Barban: 35
Buje: 21
Grožnjan: 17
Kanfanar: 30
Labin: 35
Lupoglav: 13
Medulin: 61
Motovun: 12
Opatija: 26
Pazin: 17
Poreč: 32
Pula: 57
Rovinj: 40
Umag: 31
Višnjan: 20
Vodnjan: 47
Žminj: 27
Buzet: 0
)";

int main(int argc, char *argv[]) {
  try {
    Args args = Args::parse(argc, argv);

    StateSpace state_space;
    state_space = StateSpace::parse(args.ss);

    std::cout << state_space << '\n';

    if (args.h.has_value()) {
      state_space.parse_heuristic(args.h.value());
    }

    if (args.alg == "bfs") {
      Result result = bfs(state_space);
      print_result(result, state_space);
    } else if (args.alg == "ucs") {
      Result result = ucs(state_space);
      print_result(result, state_space);
    } else { // checked in args.cpp anyway
      Result result = a_star(state_space);
      print_result(result, state_space);
    }
  } catch (const std::runtime_error &e) {
    std::cerr << e.what() << '\n';
    return EXIT_FAILURE;
  }
  return EXIT_SUCCESS;
}
