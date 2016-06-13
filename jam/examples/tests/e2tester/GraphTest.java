package e2tester;

import static org.junit.Assert.*;

import java.lang.reflect.Method;
import java.lang.reflect.ParameterizedType;
import java.lang.reflect.Type;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Set;

import org.junit.Test;

import e2soln.NoSuchNodeException;
import e2soln.Graph;
import e2soln.Node;
import edu.toronto.cs.jam.annotations.Description;

public class GraphTest {

	@Test(timeout=100)
	@Description(description="the Graph constructor")
	public void testConstructer() {
		Graph<Integer> graph = new Graph<Integer>();
	}

	// Reflection Tests
	//  prefix='testReflectionMethod'
	// Tests for the presence of methods, typing of parameters and returned
	// values

	@Test(timeout=100)
	@Description(description="the getNodes() method")
	public void testReflectionMethodGetNodes() {
		try {
			Class<?> c = Graph.class;
			Method m = c.getMethod("getNodes", new Class<?>[]{});
			Type t = m.getGenericReturnType();
			assertTrue("the return type of getNodes() should be Set<Node<T>>", t.toString().equals("java.util.Set<e2soln.Node<T>>"));
		} catch(NoSuchMethodException e) {
			fail("the getNodes() method is either private or could not be found");
		}
	}

	@Test(timeout=100)
	@Description(description="the getNode(int id) method")
	public void testReflectionMethodGetNode() {
		try {
			Class<?> c = Graph.class;
			Method m = c.getMethod("getNode", new Class<?>[]{int.class});
			Type t = m.getGenericReturnType();
			assertTrue("the return type of getNode(int) should be Node<T>", t.toString().equals("e2soln.Node<T>"));
		} catch(NoSuchMethodException e) {
			fail("the getNode(int) method is either private or could not be found");
		}
}

	@Test(timeout=100)
	@Description(description="the getNeighbours(Node<T> node) method")
	public void testReflectionMethodGetNeighbours() {
		try {
			Class<?> c = Graph.class;
			Method m = c.getMethod("getNeighbours", new Class<?>[]{Node.class});
			Type t = m.getGenericReturnType();
			assertTrue("the return type of getNeighbours(Node<T>) should be Set<Node<T>>", t.toString().equals("java.util.Set<e2soln.Node<T>>"));
		} catch(NoSuchMethodException e) {
			fail("the getNeighbours(Node<T>) method is either private or could not be found");
		}
	}

	@Test(timeout=100)
	@Description(description="the areAdjacent(int id1, int id2) method")
	public void testReflectionMethodAreAdjacentId() {
		try {
			Class<?> c = Graph.class;
			Method m = c.getMethod("areAdjacent", new Class<?>[]{int.class, int.class});
			Type t = m.getGenericReturnType();
			assertTrue("the return type of areAdjacent(int, int) should be boolean", t.equals(boolean.class));
		} catch(NoSuchMethodException e) {
			fail("the areAdjacent(int, int) method is either private or could not be found");
		}
	}

	@Test(timeout=100)
	@Description(description="the areAdjacent(Node<T> node1, Node<T> node2) method")
	public void testReflectionMethodAreAdjacentNode() {
		try {
			Class<?> c = Graph.class;
			Method m = c.getMethod("areAdjacent", new Class<?>[]{Node.class, Node.class});
			Type t = m.getGenericReturnType();
			assertTrue("the return type of areAdjacent(Node<T>, Node<T>) should be boolean", t.equals(boolean.class));
		} catch(NoSuchMethodException e) {
			fail("the areAdjacent(Node<T>, Node<T>) method is either private or could not be found");
		}
	}

	@Test(timeout=100)
	@Description(description="the getNumNodes() method")
	public void testReflectionMethodGetNumNodes() {
		try {
			Class<?> c = Graph.class;
			Method m = c.getMethod("getNumNodes", new Class<?>[]{});
			Type t = m.getGenericReturnType();
			assertTrue("the return type of getNumNodes() should be int", t.equals(int.class));
		} catch(NoSuchMethodException e) {
			fail("the getNumNodes() method is either private or could not be found");
		}
	}

	@Test(timeout=100)
	@Description(description="the getNumEdges() method")
	public void testReflectionMethodGetNumEdges() {
		try {
			Class<?> c = Graph.class;
			Method m = c.getMethod("getNumEdges", new Class<?>[]{});
			Type t = m.getGenericReturnType();
			assertTrue("the return type of getNumEdges() should be int", t.equals(int.class));
		} catch(NoSuchMethodException e) {
			fail("the getNumEdges() method is either private or could not be found");
		}
	}

	@Test(timeout=100)
	@Description(description="the addNode(int id, T value) method")
	public void testReflectionMethodAddNode() {
		try {
			Class<?> c = Graph.class;
			Method m = c.getMethod("addNode", new Class<?>[]{int.class, Object.class});
			Type t = m.getGenericReturnType();
			assertTrue("the return type of addNode(int, T) should be void", t.equals(void.class));
		} catch(NoSuchMethodException e) {
			fail("the addNode() method is either private or could not be found");
		}
	}

	@Test(timeout=100)
	@Description(description="the addEdge(Node<T> node1, Node<T> node2) method")
	public void testReflectionMethodAddEdgeNode() {
		try {
			Class<?> c = Graph.class;
			Method m = c.getMethod("addEdge", new Class<?>[]{Node.class, Node.class});
			Type t = m.getGenericReturnType();
			assertTrue("the return type of addEdge(Node<T>, Node<T> should be void", t.equals(void.class));
		} catch(NoSuchMethodException e) {
			fail("the addEdge(Node<T>, Node<T> method is either private or could not be found");
		}
	}

	@Test(timeout=100)
	@Description(description="the addEdge(int id1, int id2) method")
	public void testReflectionMethodAddEdgeId() {
		try {
			Class<?> c = Graph.class;
			Method m = c.getMethod("addEdge", new Class<?>[]{int.class, int.class});
			Type t = m.getGenericReturnType();
			assertTrue("the return type of addEdge(int, int) should be void", t.equals(void.class));
		} catch(NoSuchMethodException e) {
			fail("the addEdge(int, int) method is either private or could not be found");
		}
	}

	@Test(timeout=100)
	@Description(description="the toString() method")
	public void testReflectionMethodToString() {
		try {
			Class<?> c = Graph.class;
			Method m = c.getMethod("toString", new Class<?>[]{});
			Type t = m.getGenericReturnType();
			assertTrue("the return type of toString() should be String", t.equals(String.class));
		} catch(NoSuchMethodException e) {
			fail("the toString() method is either private or could not be found");
		}
	}

	// Method Functionality Tests
	// Tests for correct behaviour of methods

	@Test(timeout=100)
	@Description(description="a Graph with no Nodes")
	public void testGetNodesOnNewGraph() {
		Graph<Integer> g = new Graph<Integer>();
		assertEquals("a graph with no Nodes should have 0 nodes", 0, g.getNumNodes());
		assertEquals("a graph with no Nodes should have 0 edges", 0, g.getNumEdges());

		// Check that the return of getNodes is an empty set
		Set<Node<Integer>> nodes = g.getNodes();
		assertTrue("calling getNodes() on a graph with no Nodes should return an empty Set", nodes.isEmpty());
	}

	@Test(timeout=100)
	@Description(description="a Graph with a single Node")
	public void testGraphOneNode() {
		Graph<Integer> g = new Graph<Integer>();
		Node<Integer> node;
		g.addNode(1, 42);
		assertEquals("adding a new Node to a graph should increase the number of Nodes in the graph", 1, g.getNumNodes());
		assertEquals("adding a new Node to a graph should not increase the number of edges in the graph", 0, g.getNumEdges());
		assertEquals("calling getNodes() on a graph with a single Node should return a Set with a single Node", 1, g.getNodes().size());

		// Check that the Node was constructed correctly
		try {
			node = g.getNode(1);
			assertTrue("calling getNode(int) with the id of an existing Node in the graph should return that Node", node != null);
			assertEquals("the id of a Node should be the id it was added to the graph with", 1, node.getId());
			assertEquals("the value of a Node should be the value it was added to the graph with", 42, (int)node.getValue());
			assertTrue("calling getNeighbours(Node<T>) with a Node that has no neighbours should return an empty Set", g.getNeighbours(node).isEmpty());

			// Try adding an edge from this Node to itself
			try {
				g.addEdge(node, node);
				assertEquals("no self edges are allowed", 0, g.getNumEdges());
				assertTrue("no self edges are allowed", g.getNeighbours(node).isEmpty());
			} catch(NoSuchNodeException e) {
				fail("addEdge(Node<T>, Node<T>) should only throw an exception if one or both of the Nodes is not in the Graph");
			}
		} catch(NoSuchNodeException e) {
			fail("Calling getNode(int) with the id of an existing Node should not throw an exception");
		}

		// Try adding a self edge with addEdge(int id1, int id2)
		try {
			g.addEdge(1, 1);
			assertEquals("no self edges are allowed", 0, g.getNumEdges());

			try {
				node = g.getNode(1);
				assertTrue("no self edges are allowed", g.getNeighbours(node).isEmpty());
			} catch(NoSuchNodeException e) {
				fail("calling getNode(int) with the id of an existing Node should not throw an exception");
			}
		} catch(NoSuchNodeException e) {
			fail("addEdge(int, int) should only throw an exception if one or both of the Nodes with the ids provided is not in the Graph");
		}
	}

	@Test(timeout=100)
	@Description(description="a Graph with several Nodes")
	public void testGraphMultipleNodesByID() {
		Graph<String> g = new Graph<String>();
		Node<String> node;
		g.addNode(1, "first");
		g.addNode(2, "second");
		g.addNode(5, "third?");
		g.addNode(4, "fourth");
		g.addNode(3, "not third");
		assertEquals("adding new Nodes to a graph should increase the number of Nodes in the graph", 5, g.getNumNodes());
		assertEquals("adding new Nodes to a graph should not increase the number of edges in the graph", 0, g.getNumEdges());
		assertEquals("calling getNodes() on a graph should return a Set of all the Nodes in the Graph", 5, g.getNodes().size());

		// Check a few of the Nodes to ensure they were constructed
		// correctly
		try {
			node = g.getNode(1);
			assertTrue("calling getNode(int) with the id of an existing Node in the graph should return that Node", node != null);
			assertEquals("the id of a Node should be the id it was added to the graph with", 1, node.getId());
			assertEquals("the value of a Node should be the value it was added to the graph with", "first", node.getValue());
			assertTrue("calling getNeighbours(Node<T>) with a Node that has no neighbours should return an empty Set", g.getNeighbours(node).isEmpty());

			node = g.getNode(2);
			assertEquals("the id of a Node should be the id it was added to the graph with", 2, node.getId());
			assertEquals("the value of a Node should be the value it was added to the graph with", "second", node.getValue());
			assertTrue("calling getNeighbours(Node<T>) with a Node that has no neighbours should return an empty Set", g.getNeighbours(node).isEmpty());

			node = g.getNode(5);
			assertEquals("the id of a Node should be the id it was added to the graph with", 5, node.getId());
			assertEquals("the value of a Node should be the value it was added to the graph with", "third?", node.getValue());
			assertTrue("calling getNeighbours(Node<T>) with a Node that has no neighbours should return an empty Set", g.getNeighbours(node).isEmpty());
		} catch(NoSuchNodeException e) {
			fail("calling getNode(int) with the id of an existing Node should not throw an exception");
		}

		// Try adding some edges between the nodes with
		// addEdge(int, int)
		try {
			g.addEdge(1,2);
			g.addEdge(3,1);
			assertEquals("Adding new edges between Nodes in a Graph should increase the number of edges", 2, g.getNumEdges());

			// Try adding a second edge between two nodes
			g.addEdge(1,2);
			assertEquals("Only one edge can exist between two Nodes", 2, g.getNumEdges());

			// Try adding an edge symmetrically
			g.addEdge(1,5);
			g.addEdge(5,1);
			assertEquals("Only one edge can exist between two Nodes", 3, g.getNumEdges());

			// Check for adjacency with areAdjacent(int, int)
			try {
				assertTrue("Two Nodes should be adjacent when there is an edge between them", g.areAdjacent(1,2));
				assertTrue("Two Nodes should be adjacent when there is an edge between them", g.areAdjacent(2,1));

				assertTrue("Two Nodes should be adjacent when there is an edge between them", g.areAdjacent(1,3));
				assertTrue("Two Nodes should be adjacent when there is an edge between them", g.areAdjacent(3,1));

				assertTrue("Two Nodes should be adjacent when there is an edge between them", g.areAdjacent(1,5));
				assertTrue("Two Nodes should be adjacent when there is an edge between them", g.areAdjacent(5,1));

				assertFalse("Two Nodes should not be adjacent if there is no edge between them", g.areAdjacent(1,4));
				assertFalse("Two Nodes should not be adjacent if there is no edge between them", g.areAdjacent(4,1));

				assertFalse("Two Nodes should not be adjacent if there is no edge between them", g.areAdjacent(2,3));
				assertFalse("Two Nodes should not be adjacent if there is no edge between them", g.areAdjacent(3,2));

				assertFalse("Two Nodes should not be adjacent if there is no edge between them", g.areAdjacent(2,4));
				assertFalse("Two Nodes should not be adjacent if there is no edge between them", g.areAdjacent(4,2));

				assertFalse("Two Nodes should not be adjacent if there is no edge between them", g.areAdjacent(2,5));
				assertFalse("Two Nodes should not be adjacent if there is no edge between them", g.areAdjacent(5,2));

				assertFalse("Two Nodes should not be adjacent if there is no edge between them", g.areAdjacent(3,4));
				assertFalse("Two Nodes should not be adjacent if there is no edge between them", g.areAdjacent(4,3));

				assertFalse("Two Nodes should not be adjacent if there is no edge between them", g.areAdjacent(3,5));
				assertFalse("Two Nodes should not be adjacent if there is no edge between them", g.areAdjacent(5,3));

				assertFalse("Two Nodes should not be adjacent if there is no edge between them", g.areAdjacent(4,5));
				assertFalse("Two Nodes should not be adjacent if there is no edge between them", g.areAdjacent(5,4));
			} catch(NoSuchNodeException e) {
				fail("areAdjacent(int, int) should only throw an exception if one or both of the Nodes with the ids provided are not in the graph");
			}

			// Check that getNeighbours(Node<T>) returns a Set of
			// the correct size for each Node
			try {
				assertEquals("getNeighbours(Node<T>) should return a Set of all Neighbours of the Node", 3, g.getNeighbours(g.getNode(1)).size());
				assertEquals("getNeighbours(Node<T>) should return a Set of all Neighbours of the Node", 1, g.getNeighbours(g.getNode(2)).size());
				assertEquals("getNeighbours(Node<T>) should return a Set of all Neighbours of the Node", 1, g.getNeighbours(g.getNode(5)).size());
				assertEquals("getNeighbours(Node<T>) should return a Set of all Neighbours of the Node", 0, g.getNeighbours(g.getNode(4)).size());
				assertEquals("getNeighbours(Node<T>) should return a Set of all Neighbours of the Node", 1, g.getNeighbours(g.getNode(3)).size());
			} catch(NoSuchNodeException e) {
				fail("calling getNode(int) with the id of an existing Node should not throw an exception");
			}
		} catch (NoSuchNodeException e) {
			fail("addEdge(int, int) should only throw an exception if one or both of the Nodes with the ids provided are not in the Graph");
		}

	}

	@Test(timeout=100)
	@Description(description="a Graph with multiple Nodes")
	public void testGraphMultipleNodesByNode() {
		Graph<Boolean> g = new Graph<Boolean>();
		Node<Boolean> node1;
		Node<Boolean> node2;
		Node<Boolean> node3;
		Node<Boolean> node4;
		Node<Boolean> node5;
		g.addNode(1, true);
		g.addNode(2, true);
		g.addNode(5, false);
		g.addNode(4, true);
		g.addNode(3, false);
		assertEquals("adding new Nodes to a graph should increase the number of Nodes in the graph", 5, g.getNumNodes());
		assertEquals("adding new Nodes to a graph should not increase the number of edges in the graph", 0, g.getNumEdges());
		assertEquals("calling getNodes() on a graph should return a Set of all the Nodes in the Graph", 5, g.getNodes().size());

		// Check a few of the Nodes to ensure they were constructed
		// correctly
		try {
			node1 = g.getNode(1);
			assertTrue("calling getNode(int) with the id of an existing Node in the graph should return that Node", node1 != null);
			assertEquals("the id of a Node should be the id it was added to the graph with", 1, node1.getId());
			assertEquals("the value of a Node should be the value it was added to the graph with", true, node1.getValue());
			assertTrue("calling getNeighbours(Node<T>) with a Node that has no neighbours should return an empty Set", g.getNeighbours(node1).isEmpty());

			node2 = g.getNode(2);
			assertEquals("the id of a Node should be the id it was added to the graph with", 2, node2.getId());
			assertEquals("the value of a Node should be the value it was added to the graph with", true, node2.getValue());
			assertTrue("calling getNeighbours(Node<T>) with a Node that has no neighbours should return an empty Set", g.getNeighbours(node2).isEmpty());

			node3 = g.getNode(5);
			assertEquals("the id of a Node should be the id it was added to the graph with", 5, node3.getId());
			assertEquals("the value of a Node should be the value it was added to the graph with", false, node3.getValue());
			assertTrue("calling getNeighbours(Node<T>) with a Node that has no neighbours should return an empty Set", g.getNeighbours(node3).isEmpty());
		} catch(NoSuchNodeException e) {
			fail("calling getNode(int) with the id of an existing Node should not throw an exception");
		}

		// Try adding some edges between the nodes with
		// addEdge(Node<T>, Node<T>)
		try {
			// First we need to use getNode
			node1 = g.getNode(1);
			node2 = g.getNode(2);
			node3 = g.getNode(5);
			node4 = g.getNode(4);
			node5 = g.getNode(3);

			try {
				g.addEdge(node1,node2);
				g.addEdge(node3,node1);
				assertEquals("Adding new edges between Nodes in a Graph should increase the number of edges", 2, g.getNumEdges());

				// Try adding a second edge between two nodes
				g.addEdge(node1,node2);
				assertEquals("Only one edge can exist between two Nodes", 2, g.getNumEdges());

				// Try adding an edge symmetrically
				g.addEdge(node1,node5);
				g.addEdge(node5,node1);
				assertEquals("Only one edge can exist between two Nodes", 3, g.getNumEdges());

				// Check for adjacency with
				// areAdjacent(Node<T>, Node<T>)
				try {
					assertTrue("Two Nodes should be adjacent when there is an edge between them", g.areAdjacent(node1,node2));
					assertTrue("Two Nodes should be adjacent when there is an edge between them", g.areAdjacent(node2,node1));

					assertTrue("Two Nodes should be adjacent when there is an edge between them", g.areAdjacent(node1,node3));
					assertTrue("Two Nodes should be adjacent when there is an edge between them", g.areAdjacent(node3,node1));

					assertTrue("Two Nodes should be adjacent when there is an edge between them", g.areAdjacent(node1,node5));
					assertTrue("Two Nodes should be adjacent when there is an edge between them", g.areAdjacent(node5,node1));

					assertFalse("Two Nodes should not be adjacent if there is no edge between them", g.areAdjacent(node1,node4));
					assertFalse("Two Nodes should not be adjacent if there is no edge between them", g.areAdjacent(node4,node1));

					assertFalse("Two Nodes should not be adjacent if there is no edge between them", g.areAdjacent(node2,node3));
					assertFalse("Two Nodes should not be adjacent if there is no edge between them", g.areAdjacent(node3,node2));

					assertFalse("Two Nodes should not be adjacent if there is no edge between them", g.areAdjacent(node2,node4));
					assertFalse("Two Nodes should not be adjacent if there is no edge between them", g.areAdjacent(node4,node2));

					assertFalse("Two Nodes should not be adjacent if there is no edge between them", g.areAdjacent(node2,node5));
					assertFalse("Two Nodes should not be adjacent if there is no edge between them", g.areAdjacent(node5,node2));

					assertFalse("Two Nodes should not be adjacent if there is no edge between them", g.areAdjacent(node3,node4));
					assertFalse("Two Nodes should not be adjacent if there is no edge between them", g.areAdjacent(node4,node3));

					assertFalse("Two Nodes should not be adjacent if there is no edge between them", g.areAdjacent(node3,node5));
					assertFalse("Two Nodes should not be adjacent if there is no edge between them", g.areAdjacent(node5,node3));

					assertFalse("Two Nodes should not be adjacent if there is no edge between them", g.areAdjacent(node4,node5));
					assertFalse("Two Nodes should not be adjacent if there is no edge between them", g.areAdjacent(node5,node4));
				} catch(NoSuchNodeException e) {
					fail("areAdjacent(node1, node2) should only throw an exception if either node1, node2 or both Nodes are not in the graph");
				}

				// Check that getNeighbours(Node<T>) returns a
				// Set of the correct size for each Node
				assertEquals("getNeighbours(Node<T>) should return a Set of all Neighbours of the Node", 3, g.getNeighbours(node1).size());
				assertEquals("getNeighbours(Node<T>) should return a Set of all Neighbours of the Node", 1, g.getNeighbours(node2).size());
				assertEquals("getNeighbours(Node<T>) should return a Set of all Neighbours of the Node", 1, g.getNeighbours(node3).size());
				assertEquals("getNeighbours(Node<T>) should return a Set of all Neighbours of the Node", 0, g.getNeighbours(node4).size());
				assertEquals("getNeighbours(Node<T>) should return a Set of all Neighbours of the Node", 1, g.getNeighbours(node5).size());
			} catch (NoSuchNodeException e) {
				fail("addEdge(node1, node2) should only throw an exception if either node1, node2 or both Nodes are not in the Graph");
			}
		} catch (NoSuchNodeException e) {
			fail("calling getNode(int) with the id of an existing Node should not throw an exception");
		}
	}

	@Test(timeout=100)
	@Description(description="the getNode(int id) method")
	public void testGetNodeNotInGraph() {
		Graph<String> g = new Graph<String>();
		Node<String> node;
		try {
			node = g.getNode(43);
			fail("getNode(id) should throw a NoSuchNodeException if there is no Node with the ID 'id' in the Graph");
		} catch(NoSuchNodeException e) {
		}
	}

	@Test(timeout=100)
	@Description(description="the areAdjacent(int id1, int id2) method")
	public void testAreAdjacentID1NotInGraph() {
		Graph<String> g = new Graph<String>();
		g.addNode(42, "The meaning of life, the universe, and everything");
		try {
			g.areAdjacent(40,42);
			fail("areAdjacent(id1, id2) should throw a NoSuchNodeException if there is no Node with ID 'id1' in the Graph");
		} catch(NoSuchNodeException e) {
		}
	}

	@Test(timeout=100)
	@Description(description="the areAdjacent(int id1, int id2) method")
	public void testAreAdjacentID2NotInGraph() {
		Graph<Integer> g = new Graph<Integer>();
		g.addNode(99, 98);
		try {
			g.areAdjacent(99,1);
			fail("areAdjacent(id1, id2) should throw a NoSuchNodeException if there is no Node with ID 'id2' in the Graph");
		} catch(NoSuchNodeException e) {
		}
	}

	@Test(timeout=100)
	@Description(description="the areAdjacent(int id1, int id2) method")
	public void testAreAdjacentIDNoNodesInGraph() {
		Graph<Boolean> g = new Graph<Boolean>();
		try {
			g.areAdjacent(1,42);
			fail("areAdjacent(id1, id2) should throw a NoSuchNodeException if there are no Nodes with either ID 'id1' or ID 'id2' in the Graph");
		} catch(NoSuchNodeException e) {
		}
	}

	@Test(timeout=100)
	@Description(description="the areAdjacent(Node<T> node1, Node<T> node2) method")
	public void testAreAdjacentNode1NotInGraph() {
		Graph<String> g = new Graph<String>();
		g.addNode(5, "More than there are distinct tests for a method throwing an exception");
		Node<String> node1 = new Node<String>(1, "The number of tests for getNode() throwing an exception");
		Node<String> node2;
		try {
			node2 = g.getNode(5);
			try {
				g.areAdjacent(node1, node2);
				fail("areAdjacent(node1, node2) should throw a NoSuchNodeException if node1 is not in the Graph");
			} catch(NoSuchNodeException e) {
			}
		} catch(NoSuchNodeException e) {
			fail("calling getNode(int) with the id of an existing Node should not throw an exception");
		}
	}

	@Test(timeout=100)
	@Description(description="the areAdjacent(Node<T> node1, Node<T> node2) method")
	public void testAreAdjacentNode2NotInGraph() {
		Graph<Integer> g = new Graph<Integer>();
		g.addNode(75, 25);
		Node<Integer> node1;
		Node<Integer> node2 = new Node<Integer>(65, 65);
		try {
			node1 = g.getNode(75);
			try {
				g.areAdjacent(node1, node2);
				fail("areAdjacent(node1, node2) should throw a NoSuchNodeException if node2 is not in the Graph");
			} catch(NoSuchNodeException e) {
			}
		} catch(NoSuchNodeException e) {
			fail("calling getNode(int) with the id of an existing Node should not throw an exception");
		}
	}

	@Test(timeout=100)
	@Description(description="the areAdjacent(Node<T> node1, Node<T> node2) method")
	public void testAreAdjacentNodeNoNodesInGraph() {
		Graph<Boolean> g = new Graph<Boolean>();
		Node<Boolean> node1 = new Node<Boolean>(1, true);
		Node<Boolean> node2 = new Node<Boolean>(5, false);
		try {
			g.areAdjacent(node1, node2);
			fail("areAdjacent(node1, node2) should throw a NoSuchNodeException if neither node1 nor node2 are in the Graph");
		} catch(NoSuchNodeException e) {
		}
	}

	@Test(timeout=100)
	@Description(description="the addEdge(Node<T> node1, Node<T> node2) method")
	public void testAddEdgeNode1NotInGraph() {
		Graph<String> g = new Graph<String>();
		g.addNode(42, "The meaning of life, the universe, and everything");
		Node<String> node1 = new Node<String>(40, "4x10=40");
		Node<String> node2;
		try {
			node2 = g.getNode(42);
			try {
				g.addEdge(node1, node2);
				fail("addEdge(node1, node2) should throw a NoSuchNodeException if node1 is not in the Graph");
			} catch(NoSuchNodeException e) {
			}
		} catch(NoSuchNodeException e) {
			fail("calling getNode(int) with the id of an existing Node should not throw an exception");
		}
	}

	@Test(timeout=100)
	@Description(description="the addEdge(Node<T> node1, Node<T> node2) method")
	public void testAddEdgeNode2NotInGraph() {
		Graph<Integer> g = new Graph<Integer>();
		g.addNode(99, 98);
		Node<Integer> node1;
		Node<Integer> node2 = new Node<Integer>(1, 0);
		try {
			node1 = g.getNode(99);
			try {
				g.addEdge(node1, node2);
				fail("addEdge(node1, node2) should throw a NoSuchNodeException if node2 is not in the Graph");
			} catch(NoSuchNodeException e) {
			}
		} catch(NoSuchNodeException e) {
			fail("calling getNode(int) with the id of an existing Node should not throw an exception");
		}
	}

	@Test(timeout=100)
	@Description(description="the addEdge(Node<T> node1, Node<T> node2) method")
	public void testAddEdgeNodeNoNodesInGraph() {
		Graph<Boolean> g = new Graph<Boolean>();
		Node<Boolean> node1 = new Node<Boolean>(1, false);
		Node<Boolean> node2 = new Node<Boolean>(42, true);
		try {
			g.addEdge(node1, node2);
			fail("addEdge(node1, node2) should throw a NoSuchNodeException if neither node1 nor node2 are in the Graph");
		} catch(NoSuchNodeException e) {
		}
	}

	@Test(timeout=100)
	@Description(description="the addEdge(int id1, int id2) method")
	public void testAddEdgeID1NotInGraph() {
		Graph<String> g = new Graph<String>();
		g.addNode(5, "More than there are distinct tests for a method throwing this exception");
		try {
			g.addEdge(1, 5);
			fail("addEdge(id1, id2) should throw a NoSuchNodeException if there is no Node with ID 'id1' in the Graph");
		} catch(NoSuchNodeException e) {
		}
	}

	@Test(timeout=100)
	@Description(description="the addEdge(int id1, int id2) method")
	public void testAddEdgeID2NotInGraph() {
		Graph<Integer> g = new Graph<Integer>();
		g.addNode(75, 25);
		try {
			g.addEdge(75, 65);
			fail("addEdge(id1, id2) should throw a NoSuchNodeException if there is no Node with ID 'id2' in the Graph");
		} catch(NoSuchNodeException e) {
		}
	}

	@Test(timeout=100)
	@Description(description="the addEdge(int id1, int id2) method")
	public void testAddEdgeIDNoNodesInGraph() {
		Graph<Boolean> g = new Graph<Boolean>();
		try {
			g.addEdge(1, 5);
			fail("addEdge(id1, id2) should throw a NoSuchNodeException if there are no Nodes with either ID 'id1' or ID 'id2' in the Graph");
		} catch(NoSuchNodeException e) {
		}
	}
}

