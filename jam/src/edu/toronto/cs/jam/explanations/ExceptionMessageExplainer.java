package edu.toronto.cs.jam.explanations;

import java.util.regex.Matcher;
import java.util.regex.Pattern;
import org.junit.runner.notification.Failure;

/**
 * Class containing logic for cleaning up exception messages.
 * @author lungj
 *
 */
public final class ExceptionMessageExplainer {
    /**
     * Private constructor.
     */
    private ExceptionMessageExplainer() {
    }

    /**
     * Return a string that clarifies (if possible) the exception message of the
     * failure.
     * @param failure A failed JUnit test
     * @return A clarified exception message for the given failure
     */
    public static String explain(final Failure failure) {
        String message = failure.getException().getMessage();
        String failureClassName = failure.getException().getClass().getName();
        if (message == null) {
            return "";
        }
        if (failureClassName.equals("java.lang.NoClassDefFoundError")) {
            Matcher m = Pattern.compile("(.*) \\(wrong name: (.*)\\)")
                    .matcher(message);
            if (m.find()) {
                return "Class " + m.group(1).replaceAll("/", ".")
                       + " was in the wrong package. It was named "
                       + m.group(2).replaceAll("/", ".") + " instead.";
            }
            return "Unable to find class " + message.replaceAll("/", ".") + ".";
        } else if (failureClassName.equals("java.lang.IllegalAccessError")) {
            return "";
        } else if (failureClassName.equals("java.lang.NoSuchMethodError")) {
            return "";
        } else if (failureClassName.equals("java.lang.SecurityException")) {
            return "";
        } else if (failureClassName.equals("java.lang.Exception")) {
            if (message.matches("test timed out after \\d+ milliseconds")) {
                return "";
            }
        }
        return message;
    }

}
