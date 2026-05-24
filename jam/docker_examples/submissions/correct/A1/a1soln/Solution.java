package a1soln;

/** Reference solution: passes all tests. */
public final class Solution {

    private Solution() {
        // utility
    }

    public static int safeSum(int[] nums) {
        int total = 0;
        for (int n : nums) {
            total += n;
        }
        return total;
    }

    public static double safeAverage(int[] nums) {
        if (nums.length == 0) {
            return 0.0;
        }
        return (double) safeSum(nums) / nums.length;
    }
}
