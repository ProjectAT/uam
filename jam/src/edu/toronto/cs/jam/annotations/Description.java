package edu.toronto.cs.jam.annotations;

import java.lang.annotation.Retention;
import java.lang.annotation.Target;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.ElementType;

/**
 * Annotations used for reporting by JAM.
 * @author lungj
 *
 */
@Retention(RetentionPolicy.RUNTIME)
@Target({ElementType.METHOD})
public @interface Description {
    /**
     * A description of the test case.
     */
    String description() default "";
}
