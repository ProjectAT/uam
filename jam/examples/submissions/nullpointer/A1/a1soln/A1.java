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
    if (list.size() > 1) {
	myList = list;     // but not always
    }
    for (T curr: myList) {
      if (curr.equals(elt)) {
        return true;
      }
    }
    return false;
  }
}
