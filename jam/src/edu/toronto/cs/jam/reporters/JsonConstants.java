package edu.toronto.cs.jam.reporters;
import com.google.gson.JsonObject;

public class JsonConstants {

    public final static String DESCRIPTION = "description";
    public final static String MESSAGE = "message";
    public final static String DETAILS = "details";
    public final static String PASSES = "passes";
    public final static String ERRORS = "errors";
    public final static String FAILURES = "failures";
    public final static String DATE = "date";
    public final static String ASSIGNMENT = "assignment";
    public final static String STUDENTS = "students";
    public final static String RESULTS = "results";
    public final static String TESTS = "tests";

    /**
     * Return a fake student Json.
     * @return A JsonObject with place-holder student information
     */
    public static JsonObject fakeStudent() {
	JsonObject student = new JsonObject();
        student.addProperty("utorid", "");
        student.addProperty("first", "");
        student.addProperty("last", "");
        student.addProperty("id", "0000000000");
        student.addProperty("section", "");
        student.addProperty("source", "");
        student.addProperty("email", "");
	return student;
    }
}
