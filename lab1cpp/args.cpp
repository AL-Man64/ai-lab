#include "args.hpp"
#include <stdexcept>

Args Args::parse(int argc, char *argv[]) {
  std::optional<std::string> alg;
  std::optional<std::string> ss;
  std::optional<std::string> h;
  bool check_optimistic = false;
  bool check_consistent = false;

  int i = 0;
  while (i < argc) {
    std::string arg(argv[i]);
    if (arg == "--check-optimistic") {
      check_optimistic = true;
    } else if (arg == "--check-consistent") {
      check_consistent = true;
    } else if (arg == "--alg") {
      i += 1;
      if (i >= argc) {
        break;
      }
      std::string val(argv[i]);
      alg = val;
    } else if (arg == "--ss") {
      i += 1;
      if (i >= argc) {
        break;
      }
      std::string val(argv[i]);
      ss = val;
    } else if (arg == "-h") {
      i += 1;
      if (i >= argc) {
        break;
      }
      std::string val(argv[i]);
      h = val;
    }

    i += 1;
  }

  if (!alg.has_value() || !ss.has_value()) {
    throw std::runtime_error(
        "Necessary arguments --algorithm and --ss missing");
  }

  if (!(alg.value() == "bfs") && !(alg.value() == "ucs") &&
      !(alg.value() == "astar")) {
    throw std::runtime_error(
        R"(Argument --algorithm can only take values "bfs", "ucs" or "astar")");
  }

  return Args(alg.value(), ss.value(), h, check_optimistic, check_consistent);
}
