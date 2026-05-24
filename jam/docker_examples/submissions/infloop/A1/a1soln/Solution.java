package a1soln;

/** Spins forever. Only safe to run with docker_enabled = True. */
public final class Solution {

    private Solution() {
    }

    public static int safeSum(int[] nums) {
        long spin = 0;
        while (true) {
            spin++; // prevent the JIT from optimising the loop away
        }
    }

    public static double safeAverage(int[] nums) {
        return safeSum(nums);
    }
}
