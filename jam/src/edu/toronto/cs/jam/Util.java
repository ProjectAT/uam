package edu.toronto.cs.jam;

/**
 * Utility functions.
 * @author lungj
 *
 */
public class Util {
    /**
     * Return true iff str starts with a vowel.
     * @param str String to check
     * @return boolean
     */
    public static boolean startsWithVowel(String str) {
        return "AEIOUaeiou".indexOf(str.substring(0, 1)) > -1;
    }
}
