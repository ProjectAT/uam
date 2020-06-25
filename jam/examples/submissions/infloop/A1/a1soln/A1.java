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
    for (int i=0; i < list.size(); ) {  // INF LOOP
      if (list.get(i).equals(elt)) {
        return true;
      }
    }
    return false;
  }
}
