package a1tester;

import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;

import java.util.ArrayList;
import java.util.List;

import org.junit.Before;
import org.junit.Test;

import edu.toronto.cs.jam.annotations.Description;

import a1soln.A1;

public class A1Test {

  public static final int TIMEOUT = 2;

  List<String> list;
  A1 a1 = new A1();

  @Before
  public void setUp() {
    list = new ArrayList<>();
  }

  @Test(timeout=TIMEOUT)
  @Description(description="empty input list")
  public void testEmpty() {
    assertFalse("An empty list contains \"42\"!",
        a1.myContains(list, "42"));
  }

  @Test(timeout=TIMEOUT)
  @Description(description="singleton input list that contains the element")
  public void testSingletonPresent() {
    list.add("42");
    assertTrue("A list [\"42\"] does not contain \"42\"!",
        a1.myContains(list, "42"));
  }

  @Test(timeout=TIMEOUT)
  @Description(description="singleton input list that does not contain the element")
  public void testSingletonNotPresent() {
    list.add("24");
    assertFalse("A list [\"24\"] contains \"42\"!",
        a1.myContains(list, "42"));
  }

  @Test(timeout=TIMEOUT)
  @Description(description="longer list that does not contain the element")
  public void testLongerNotPresent() {
    list.add("foo");
    list.add("bar");
    list.add("foobar");
    assertFalse("A list [\"foo\", \"bar\", \"foobar\"] contains \"42\"!",
        a1.myContains(list, "42"));
  }

  @Test(timeout=TIMEOUT)
  @Description(description="longer list that contains the element")
  public void testLongerPresent() {
    list.add("foo");
    list.add("bar");
    list.add("42");
    list.add("foobar");
    assertTrue("A list [\"foo\", \"bar\", \"42\", \"foobar\"] does not contain \"42\"!",
        a1.myContains(list, "42"));
  }
}
