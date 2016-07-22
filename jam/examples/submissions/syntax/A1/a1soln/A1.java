package a1soln;

import java.util.List;

public class A1 {

  /**
   * A silly method used to demonstrate JAM.
   * @param list
   * @param elt
   * @return
   */
  public <T> boolean myContains (List<T> list, T elt) {
    I AM A SYNTAX ERROR
    for (T curr: list) {
      if (curr.equals(elt)) {
        return true;
      }
    }
    return false;
  }
}
