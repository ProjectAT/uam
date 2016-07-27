package edu.toronto.cs.jam.reporters;

import java.io.PrintStream;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.junit.runner.Result;
import org.junit.runner.notification.Failure;
import org.junit.runner.notification.RunListener;

import edu.toronto.cs.jam.Util;
import edu.toronto.cs.jam.annotations.Description;
import edu.toronto.cs.jam.explanations.ExceptionExplainer;
import edu.toronto.cs.jam.explanations.ExceptionMessageExplainer;
import edu.toronto.cs.jam.explanations.ExceptionRenamer;
import edu.toronto.cs.jam.reporters.JsonConstants;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonObject;
import com.google.gson.JsonArray;
import com.google.gson.JsonPrimitive;

/**
 * Generate a JSON object to a text file containing the names and
 * results of the unit tests that this Listener was listening to, as
 * well as placeholder student information that is expected by UAM.
 */
public class JSonOutputListener extends RunListener {

    /**
     * PrintStream for output of results
     */
    private PrintStream output;

    /**
     * Map: testClassName to {Map: testMethodName to TestInfo object}
     */
    private Map<String, Map<String,TestInfo>> testInfo = 
	new HashMap<String, Map<String, TestInfo>>();

    /**
     * Set output to the provided PrintStream printStream.
     * @param printStream A PrintStream
     */
    public JSonOutputListener(final PrintStream printStream) {
        this.output = printStream;
    }

    /**
     * Set output to the provided PrintStream printStream and update
     * the ExceptionExplainer explanations with the provided file
     * path.
     * @param printStream A PrintStream
     * @param explanationFilePath Path to an exception explanation XML document
     */
    public JSonOutputListener(final PrintStream printStream,
                              final String explanationFilePath) {
        this.output = printStream;
        ExceptionExplainer.updateExplanations(explanationFilePath);
    }

    /**
     * If a run started, record a new test as "passed" (for now).
     * In case of an initializationError (this results from a student
     * submission not compiling), record all methods for the class
     * as failures.
     * @param desc A junit Description for a test
     */
    public final void testStarted(final org.junit.runner.Description desc) 
	throws java.lang.Exception {
	super.testStarted(desc);

	String className = desc.getClassName();
	boolean passed = true;

	if (isCompilationError(desc)) {
	    passed = false;
	}

	String description = description(desc);
	
	// make the key in the Map a fully qualified method name
	String methodName = qualifiedName(desc);

	TestInfo thisInfo = new TestInfo(methodName, 
					 description, 
					 passed);
	if (testInfo.containsKey(className)) {
	    testInfo.get(className).put(methodName, thisInfo);
	} else {
	    Map<String, TestInfo> thisInfoMap = new HashMap<String, TestInfo>();
	    thisInfoMap.put(methodName, thisInfo);
	    testInfo.put(className, thisInfoMap);
	}
    }

    /**
     * Record that this test failed.
     * @param failure A failed JUnit test
     */
    public final void testFailure(final Failure failure)
	throws java.lang.Exception {
	super.testFailure(failure);

	recordOneFailure(failure,
			 failure.getDescription().getClassName(), 
			 qualifiedName(failure.getDescription()));
    }

    private void recordOneFailure(final Failure failure, String className,
				  String methodName) {
        testInfo.get(className).get(methodName).failed();
    }

    /**
     * Output a JSON object as a string to the PrintStream 'output' that
     * contains test results separated into passes, failures and errors, with
     * appropriate information, for each test class.
     * @param result Result from running the test suite
     */
    public final void testRunFinished(final Result result) {
        Gson gson = new GsonBuilder()
                .disableHtmlEscaping()
                .setPrettyPrinting()
                .create();
	JsonObject wrapper = new JsonObject();
        JsonArray studentsArray = new JsonArray();
        JsonObject student = JsonConstants.fakeStudent();

        // Add the student JsonObject to the students JsonArray
        studentsArray.add(student);

        // Add the studentsArray JsonArray to the wrapper JsonObject
        wrapper.add(JsonConstants.STUDENTS, studentsArray);

	// Collect test results as passes and failures, per test class.
        JsonObject testresults = collectResults(result);

        // Add the testresults JsonObject to the wrapper JsonObject
        wrapper.add(JsonConstants.RESULTS, testresults);

        // Add date and assignment pair placeholders to the wrapper JsonObject
        wrapper.addProperty(JsonConstants.DATE, "");
        wrapper.addProperty(JsonConstants.ASSIGNMENT, "");

        // Output the serialized wrapper JsonObject
        output.print(gson.toJson(wrapper));
    }

    /**
     * Take a useless List<Failures> from the Result object, and
     * build and return a Map: qualifiedTestName -> Failure
     * @param result The result of a complete unit test run.
     * @return A Map: qualifiedTestName -> Failure
     */
    private Map<String, Failure> failuresMap(final Result result) {
	List<Failure> failures = 
	    new ArrayList<Failure>(result.getFailures());
	Map<String, Failure> failureMap = new HashMap<String, Failure>();

	for (Failure failure: failures) {
	    failureMap.put(qualifiedName(failure.getDescription()),
			   failure);
	}
	return failureMap;
    }

    /**
     * Create and return a JsonObject that contains, for each test class,
     * all passes, failures, and errors (empty in JUnit4!).
     * @param result The JUnit Result object from running all unit tests
     * @return A JsonObject that contains, for each test class, all passes,
     * failures, and errors (errors are empty in JUnit4). Each pass contains
     * a description of the test. Each failure contains a description of the
     * failed test, an error message (message from JUnit's Failure object,
     * substituted with Exception name if Failure's message is null -- as with
     * a NullPointerException, for example), and a trace.
     */
    private JsonObject collectResults(final Result result) {
	JsonObject testResults = new JsonObject();
	Map<String, Failure> failureMap = failuresMap(result);
	
	// for each test class
	for (String className: testInfo.keySet()) {
	    JsonObject testResult = new JsonObject();
	    JsonObject passes = new JsonObject();
	    JsonObject failures = new JsonObject();
	    JsonObject errors = new JsonObject();  // there are no errors in JUnit 4
	    Map<String, TestInfo> testClassInfo = testInfo.get(className);	    

	    // for each test method in test class
	    for (String methodName: testClassInfo.keySet()) {
		TestInfo testMethodInfo = testClassInfo.get(methodName);
		if (testMethodInfo.passed) {
		    passes.add(methodName,
			       new JsonPrimitive(testMethodInfo.description));
		} else {
		    Failure failure = 
			failureMap.get(testMethodInfo.qualifiedName);
		    JsonObject failJson = new JsonObject();
		    failJson.addProperty(JsonConstants.DESCRIPTION,
					 testMethodInfo.description);
		    failJson.addProperty(JsonConstants.MESSAGE,
					 isCompilationError(failure) ? "" : ExceptionExplainer.failureMessage(failure));
		    failJson.addProperty(JsonConstants.DETAILS, 
					 isCompilationError(failure) ? "" : failure.getTrace());
		    failures.add(methodName, failJson);
		}
	    }
	    testResult.add(JsonConstants.PASSES, passes);
	    testResult.add(JsonConstants.FAILURES, failures);
	    testResult.add(JsonConstants.ERRORS, errors);  // does it have to be there?
	    testResults.add(className, testResult);
	}
	return testResults;
    }

    /**
     * Return a qualified name of class:methodname for a description.
     * @param desc A org.junit.runner.Description
     * @return A qualified name of class:methodname for the given description
     */
    private String qualifiedName(final org.junit.runner.Description desc) {
        return desc.getClassName() + "." + desc.getMethodName();
    }

    private String description(final org.junit.runner.Description desc) {

    	if (isCompilationError(desc)) { 
	    return ExceptionExplainer.COMPILE_ERROR_MSG;
	}
	return desc.getAnnotation(Description.class).description();
    }

    private boolean isCompilationError(final org.junit.runner.Description desc) {
	// TODO: is there a better way?
	return desc.getMethodName().equals("initializationError");
    }

    private boolean isCompilationError(final Failure failure) {
	return isCompilationError(failure.getDescription());
    }

    
    /**
     * Info about a Test Method.
     */
    private class TestInfo {
	/* 
	 * Full qualified name of the unit test.
	 */
	String qualifiedName;

	/*
	 * Whether the test passed or not.
	 */
	boolean passed;

	/*
	 * Description of the test.
	 */
	String description;

	/*
	 * Create a TestInfo with the given name and description.
	 */
	TestInfo(String qualifiedName, String description, boolean passed) {
	    this.qualifiedName = qualifiedName;
	    this.passed = passed;
	    this.description = description;
	}

	/*
	 * Mark that this unit test failed.
	 */
	void failed() {
	    this.passed = false;
	}

	@Override
	public String toString() {
	    return (this.qualifiedName + ": " +
		    this.description + " " + 
		    this.passed); 
	}
    }
}
