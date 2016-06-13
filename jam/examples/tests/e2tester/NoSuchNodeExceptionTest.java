package e2tester;

import static org.junit.Assert.*;
import org.junit.Test;

import e2soln.NoSuchNodeException;
import edu.toronto.cs.jam.annotations.Description;

public class NoSuchNodeExceptionTest {
	@Test(timeout=50)
	@Description(description="the NoSuchNodeException constructor with no arguments")
	public void testConstructorNoArgs() {
		new NoSuchNodeException();
	}

	@Test(timeout=50)
	@Description(description="the NoSuchNodeException constructor with one argument")
	public void testConstructorOneArg() {
		new NoSuchNodeException("Message");
	}

	@Test(timeout=50)
	@Description(description="that NoSuchNodeException is a checked exception")
	public void testIsCheckedException() {
		Object e = new NoSuchNodeException();
		if ((!(e instanceof Exception)) || (e instanceof RuntimeException)) {
			fail("EdgeException must be a checked exception.");
		}
	}

}
