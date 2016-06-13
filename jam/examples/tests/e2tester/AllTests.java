package e2tester;

import org.junit.runner.RunWith;
import org.junit.runners.Suite;
import org.junit.runners.Suite.SuiteClasses;

@RunWith(Suite.class)
@SuiteClasses({ NoSuchNodeExceptionTest.class, GraphTest.class })
public class AllTests {

}
