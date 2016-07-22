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
    assertFalse("myContains(empty list, \"42\") should be false.",
        a1.myContains(list, "42"));
  }

  @Test(timeout=TIMEOUT)
  @Description(description="singleton input list that contains the element")
  public void testSingletonPresent() {
    list.add("42");
    assertTrue("myContains([\"42\"], \"42\") should be true.",
        a1.myContains(list, "42"));
  }

  @Test(timeout=TIMEOUT)
  @Description(description="singleton input list that does not contain the element")
  public void testSingletonNotPresent() {
    list.add("24");
    assertFalse("myContains([\"24\"], \"42\") should be false.",
        a1.myContains(list, "42"));
  }

  @Test(timeout=TIMEOUT)
  @Description(description="longer list that does not contain the element")
  public void testLongerNotPresent() {
    list.add("foo");
    list.add("bar");
    list.add("foobar");
    assertFalse("myContains([\"foo\", \"bar\", \"foobar\"], \"42\") should be false.",
        a1.myContains(list, "42"));
  }

  @Test(timeout=TIMEOUT)
  @Description(description="longer list that contains the element")
  public void testLongerPresent() {
    list.add("foo");
    list.add("bar");
    list.add("42");
    list.add("foobar");
    assertTrue("myContains([\"foo\", \"bar\", \"42\", \"foobar\"], \"42\") should be true.",
        a1.myContains(list, "42"));
  }
}
