package ui;

import java.io.FileNotFoundException;

/**
 * Program
 */
public class Program {

  private static void tryStuff() throws FileNotFoundException {
  }

  public static void run(String[] args) throws FileNotFoundException {
    tryStuff();
    if (args[0].equals("resolution")) {
      Algorithms.resolution(args[1]);
    } else if (args[0].equals("cooking")) {
      Algorithms.cooking(args[1], args[2]);
    } else {
      throw new UnsupportedOperationException("The program only supports 'resolution' and 'cooking'");
    }
  }

}
