package a1soln;

import java.util.ArrayList;
import java.util.List;

/** Allocates ~1 GiB. Only safe to run with docker_enabled = True. */
public final class Solution {

    private Solution() {
    }

    private static void eatMemory() {
        List<byte[]> chunks = new ArrayList<>();
        for (int i = 0; i < 64; i++) {              // 64 * 16 MiB = 1 GiB
            chunks.add(new byte[16 * 1024 * 1024]);
        }
    }

    public static int safeSum(int[] nums) {
        eatMemory();
        return 0;
    }

    public static double safeAverage(int[] nums) {
        eatMemory();
        return 0.0;
    }
}
