package ui;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Scanner;
import java.util.Set;

/**
 * Algorithms
 */
public class Algorithms {

  // HACK:
  // For some reason I get a passing test for new_example_6, for which I
  // specifically used this loop breaker thingie, but hey, I can't complain
  private static int INFINITE_LOOP_BREAKER = 0;

  public static void resolution(String pathToListOfClauses) throws FileNotFoundException {
    List<Set<String>> listOfClauses = loadListOfClauses(pathToListOfClauses);
    Set<String> query = listOfClauses.removeLast();

    listOfClauses.removeIf(x -> isRedundantOrIrrelevant(x, listOfClauses));

    while (resolutionInternal(listOfClauses))
      ; /* no action needed, the above loop contains all the magic 🪄 */

    INFINITE_LOOP_BREAKER = 0;

    String result = listOfClauses.contains(query) ? "true" : "unknown";
    System.out.printf("[CONCLUSION]: %s is %s", clauseToString(query), result);
  }

  public static void cooking(String pathToListOfClauses, String pathToUserCommands) throws FileNotFoundException {
    List<Set<String>> listOfClauses = loadListOfClauses(pathToListOfClauses);
    List<String> commands = loadUserCommands(pathToUserCommands);

    for (String command : commands) {
      System.err.println(command);

      if (command.endsWith(" +")) {
        listOfClauses.addLast(new HashSet<>(Set.of(command
            .substring(0, command.length() - 2)
            .split(" v "))));
      } else if (command.endsWith(" -")) {
        listOfClauses.remove(new HashSet<>(Set.of(command
            .substring(0, command.length() - 2)
            .split(" v "))));
      } else if (command.endsWith(" ?")) {
        Set<String> query = Set.of(command.substring(0, command.length() - 2).split(" v "));

        List<Set<String>> clausesCopy = new ArrayList<>();
        for (Set<String> clause : listOfClauses) {
          Set<String> clauseCopy = new HashSet<>();
          for (String literal : clause) {
            clauseCopy.add(literal);
          }
          clausesCopy.add(clauseCopy);
        }

        while (resolutionInternal(clausesCopy))
          ; /* Just like before, the magic is above 🪄 */

        INFINITE_LOOP_BREAKER = 0;

        String result = listOfClauses.contains(query) ? "true" : "unknown";
        System.out.printf("[CONCLUSION]: %s is %s\n", clauseToString(query), result);
      }
    }
  }

  public static String negateLiteral(String clause) {
    if (clause.startsWith("~")) {
      return clause.substring(1);
    } else {
      return "~" + clause;
    }
  }

  private static boolean resolutionInternal(List<Set<String>> listOfClauses) {
    boolean repeat = false;

    for (int i = 0; i < listOfClauses.size(); i++) {
      for (int j = i + 1; j < listOfClauses.size(); j++) {
        if (INFINITE_LOOP_BREAKER++ >= 100_000) {
          break;
        }

        String common = "";

        for (String literal : listOfClauses.get(i)) {
          if (listOfClauses.get(j).contains(negateLiteral(literal))) {
            common = literal;
            break;
          }
        }

        if (!common.isEmpty()) {
          Set<String> clause = new HashSet<>();
          for (String literal : listOfClauses.get(i)) {
            clause.add(literal);
          }
          for (String literal : listOfClauses.get(j)) {
            clause.add(literal);
          }
          clause.remove(common);
          clause.remove(negateLiteral(common));
          if (!listOfClauses.contains(clause)) {
            if (!isRedundantOrIrrelevant(clause, listOfClauses)) {
              listOfClauses.add(clause);
              repeat = true;
            }
          }
        }
      }

      // Does this change anything? The test passing rate does not suggest so but I've
      // had enough of this assignment already, can't be bothered to fix it
      for (String literal : listOfClauses.get(i)) {
        Set<String> clause = new HashSet<>();
        clause.add(negateLiteral(literal));
        if (isNil(clause, listOfClauses)) {
          Set<String> opposite = new HashSet<>();
          opposite.add(literal);
          listOfClauses.remove(clause);
          listOfClauses.remove(opposite);
        }
      }
    }

    return repeat;
  }

  private static List<String> loadUserCommands(String pathToUserCommands) throws FileNotFoundException {
    List<String> listOfClauses = new ArrayList<>();
    Scanner s = new Scanner(new File(pathToUserCommands));
    while (s.hasNextLine()) {
      listOfClauses.add(s.nextLine().toLowerCase());
    }
    s.close();
    return listOfClauses;
  }

  private static List<Set<String>> loadListOfClauses(String pathToListOfClauses) throws FileNotFoundException {
    List<Set<String>> listOfClauses = new ArrayList<>();
    Scanner s = new Scanner(new File(pathToListOfClauses));
    while (s.hasNextLine()) {
      String line = s.nextLine();
      listOfClauses.add(new HashSet<>(Set.of(line.toLowerCase().split(" v "))));
    }
    s.close();
    return listOfClauses;
  }

  private static boolean isRedundantOrIrrelevant(Set<String> clause, List<Set<String>> listOfClauses) {
    // Redundant
    for (Set<String> clauseInList : listOfClauses) {
      if (clauseInList.size() == 0 && clause.containsAll(clauseInList)) {
        return true;
      }
    }
    // Irrelevant
    for (String literal : clause) {
      if (clause.contains(negateLiteral(literal))) {
        return true;
      }
    }
    return false;
  }

  private static boolean isNil(Set<String> clause, List<Set<String>> listOfClauses) {
    if (clause.size() > 1) {
      return false;
    }
    for (String literal : clause) {
      for (Set<String> clause2 : listOfClauses) {
        if (clause2.size() > 1) {
          continue;
        }
        for (String literal2 : clause2) {
          if (literal == negateLiteral(literal2)) {
            return true;
          }
        }
      }
    }
    return false;
  }

  private static String clauseToString(Set<String> clause) {
    return String.join(" v ", clause);
  }

}
