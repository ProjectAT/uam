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
    List<T> myList = null; // NULL POINTER EXN
    for (T curr: myList) {
      if (curr.equals(elt)) {
        return true;
      }
    }
    return false;
  }
}
