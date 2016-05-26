/**
 * 
 */
package e2soln;

/**
 * A node in a Graph<T>.
 * @author anya
 */
public class Node<T> implements Comparable<Node<T>>{

  private int id; // the ID of this Node
  private T value; // the value stored in this Node

  /**
   * Creates a new Node with the given ID and value.
   * @param id the ID of the new Node.
   * @param value the value of the new Node.
   */
  public Node(int id, T value) {
    this.id = id;
    this.value = value;
  }

  /**
   * Returns the ID of this Node.
   * @return the ID of this Node.
   */
  public int getId() {
    return id;
  }

  /**
   * Returns the value of this Node.
   * @return the value of this Node
   */
  public T getValue() {
    return value;
  }

  /**
   * Sets the value of this Node to value.
   * @param the new value of this Node
   */
  public void setValue(T value) {
    this.value = value;
  }

  @Override
  public String toString() {
    return "(" + id + ", " + value.toString() + ")";
  }

  /**
   * Compares this Node to Node other. Comparison is based on comparison
   * of Node IDs.
   * @return an int < 0, if ID of this Node is less than ID of other
   *         0, if ID of this Node is equal to ID of other
   *         an int > 0, otherwise
   */
  @Override
  public int compareTo(Node<T> other) {
    return id - other.id;
  }
}