#pragma once

#include <optional>
#include <string>

class Args {
public:
  static Args parse(int argc, char *argv[]);

  std::string alg;
  std::string ss;
  std::optional<std::string> h;
  bool check_optimistic;
  bool check_consistent;

private:
  Args(std::string algorithm, std::string ss, std::optional<std::string> h,
       bool check_optimistic, bool check_consistent)
      : alg(algorithm), ss(ss), h(h), check_consistent(check_consistent),
        check_optimistic(check_optimistic) {}
};
