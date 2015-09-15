package org.junit.runner;

import java.io.FileNotFoundException;
import java.io.PrintStream;

import java.util.Arrays;

import org.junit.internal.RealSystem;
import org.junit.internal.JUnitSystem;

import edu.toronto.cs.jam.reporters.JSonOutputListener;


public class JAMCore extends JUnitCore {
    public final static String DEFAULT_JSON_FILE = "result.json";

    /**
     * Set up a JUnitSystem and overlaying JAMCore with a JSonOutputListener
     * to generate JSON output from the results of running the provided
     * test suite(s). If more than 1 argument is provided, the last argument
     * is expected to be a path to an XML file containing exception
     * explanations.
     * @param args A list of paths to test suite(s) and possibly an XML file
     */
    public static void main(final String... args) {
        JAMCore core = new JAMCore();
        JUnitSystem system = new RealSystem();
        Result result;

        // If more than one argument is provided, expect the last
        // argument to be a path to an XML file containing exception
        // explanations. Pass it in separately when adding the listener
        // and do not pass it to runMain()
        try {
            if (args.length > 1) {
                core.addListener(new JSonOutputListener(
                        new PrintStream(DEFAULT_JSON_FILE), args[args.length - 1]));
            } else {
                core.addListener(new JSonOutputListener(
                        new PrintStream(DEFAULT_JSON_FILE)));
            }
        } catch (FileNotFoundException e) {
            System.err.println("Unable to open report file for writing. " +
			       e.toString());
            System.exit(1);
        }

        if (args.length > 1) {
            result = core.runMain(system,
                                  Arrays.copyOfRange(args, 0, args.length - 1));
        } else {
            result = core.runMain(system, args);
        }

        if (result.wasSuccessful()) {
            System.exit(0);
        } else {
            System.exit(1);
        }
    }

    /**
     * Run the provided test suites and return the Result.
     * @param system A JUnitSystem
     * @param args A list of paths to JUnit test suites
     * @return The result of running the test suites
     */
    final Result runMain(final JUnitSystem system, final String... args) {
        JUnitCommandLineParseResult jUnitCommandLineParseResult =
                JUnitCommandLineParseResult.parse(args);

        return run(jUnitCommandLineParseResult
                .createRequest(defaultComputer()));
    }

    /**
     * Return a new Computer.
     * @return A new Computer
     */
    static Computer defaultComputer() {
        return new Computer();
    }
}
