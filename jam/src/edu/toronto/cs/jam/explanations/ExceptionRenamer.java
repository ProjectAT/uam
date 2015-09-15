package edu.toronto.cs.jam.explanations;

import org.junit.runner.notification.Failure;

/**
 * Rename an Exception for the purposes of feedback from unit testing.
 * @author lungj
 *
 */
public final class ExceptionRenamer {
    /**
     * Private constructor.
     */
    private ExceptionRenamer() {
    }


    /**
     * If the provided Failure was caused by a java.lang.Exception Exception,
     * if it was actually a TimeoutException before returning the Simple Name
     * of the Exception that caused the Failure.
     * i.e. Rename TimeoutExceptions
     * @param failure A failed JUnit test
     * @return The name of the exception that caused the test failure
     */
    public static String rename(final Failure failure) {
        String fullName = failure.getException().getClass().getName();
        String message = failure.getException().getMessage();

        if (fullName.equals("java.lang.Exception")) {
            // This was a generic timeout exception from JUnit.
            if (message.matches("test timed out after \\d+ milliseconds")) {
                return "TimeoutException";
            }
        }

        return failure.getException().getClass().getSimpleName();
    }
}
