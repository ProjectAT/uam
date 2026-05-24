package a1soln;

/** Buggy solution: off-by-one in safeSum, wrong empty-list contract. */
public final class Solution {

    private Solution() {
    }

    public static int safeSum(int[] nums) {
        int total = 1; // off by one
        for (int n : nums) {
            total += n;
        }
        return total;
    }

    public static double safeAverage(int[] nums) {
        // Spec says return 0.0 on empty; this throws instead.
        return (double) safeSum(nums) / Math.max(nums.length - 1, 1);
    }
}
