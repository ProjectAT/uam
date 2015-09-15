package e2soln;

public class E2 {

  /**
   * Creates and prints the Graph in the handout. Demonstrates
   * behaviour of some of the required methods.
   * @param args ignored
   */
  public static void main(String[] args) {
    Graph<String> graph = new Graph<>();

    System.out.println(graph); // initially empty

    for (int i=1; i<=6; i++) {
      graph.addNode(i, "value" + i);
    }

    try { // these should be added
      graph.addEdge(1, 2);
      graph.addEdge(1, 5);
      graph.addEdge(2, 5);
      graph.addEdge(2, 3);
      graph.addEdge(4, 3);
      graph.addEdge(4, 5);
      graph.addEdge(4, 6);
    } catch (NoSuchNodeException e) {
      e.printStackTrace();
    }

    System.out.println(graph);

    // this one should not be added
    try {
      graph.addEdge(5, 1);
    } catch (NoSuchNodeException e) {
      e.printStackTrace();
    }

    System.out.println(graph);

    // this should throw an exception
    try {
      graph.addEdge(42, 2);
    } catch (NoSuchNodeException e1) {
      System.out.println("No such node: " + e1.getMessage());
    }

    try { // these are safe
      System.out.println("1 and 2? " + graph.areAdjacent(1, 2));
      System.out.println("2 and 6? " + graph.areAdjacent(2, 6));
      System.out.println("3 and 4? " + graph.areAdjacent(3, 4));
    } catch (NoSuchNodeException e) {
      e.printStackTrace();
    }    
  }
}
