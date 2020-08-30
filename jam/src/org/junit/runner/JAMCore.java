package org.junit.runner;

import java.io.FileNotFoundException;
import java.io.PrintStream;

import java.util.Arrays;

import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.CommandLineParser;
import org.apache.commons.cli.DefaultParser;
import org.apache.commons.cli.HelpFormatter;
import org.apache.commons.cli.Option;
import org.apache.commons.cli.Options;
import org.apache.commons.cli.ParseException;

import org.junit.internal.RealSystem;
import org.junit.internal.JUnitSystem;

import edu.toronto.cs.jam.reporters.JSonOutputListener;


public class JAMCore extends JUnitCore {
    public final static String DEFAULT_JSON_FILE = "result.json";

    /**
     * @param args A list of paths to test suite(s) 
     * and optional output file name and exception explainer.
     */
    public static void main(final String... args) {
        JAMCore core = new JAMCore();
        JUnitSystem system = new RealSystem();
        Result result;

	// Parse command line arguments
	Options options = new Options();

        Option output = new Option("o", "output", true, "output file");
        output.setRequired(false);  // not mandatory
        options.addOption(output);

        Option exceptions = new Option("e", "exceptions", true, "exceptions explainer");
        exceptions.setRequired(false);  // not mandatory
        options.addOption(exceptions);

        CommandLineParser parser = new DefaultParser();
        HelpFormatter formatter = new HelpFormatter();
        CommandLine cmd = null;

        try {
            cmd = parser.parse(options, args);
	} catch (ParseException e) {
            System.out.println(e.getMessage());
            formatter.printHelp("JAMCore", options);
            System.exit(1);
        }
	
	String outputFilePath = cmd.getOptionValue("output", DEFAULT_JSON_FILE);
	String exceptionExplainer = cmd.getOptionValue("exceptions", "");  // TODO: change with JsonOutputListener 
	String [] testers = cmd.getArgs(); // the rest of command-line arguments

	// Set up corresponding Listener.
        try {
            if (exceptionExplainer.equals("")) {
                core.addListener(new JSonOutputListener(
                        new PrintStream(outputFilePath)));
            } else {
                core.addListener(new JSonOutputListener(
                        new PrintStream(outputFilePath), exceptionExplainer));
            }
        } catch (FileNotFoundException e) {
            System.err.println("Unable to open report file for writing. " +
			       e.toString());
            System.exit(1);
        }

	// run the testers
	result = core.runMain(system, testers);

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
