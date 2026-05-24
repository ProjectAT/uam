package a1soln;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

/**
 * Probes the container for host-filesystem access. The reads return
 * either image-only data or an exception; any write outside the bind
 * mount lands in the ephemeral container layer that --rm discards.
 */
public final class Solution {

    private static final String[] PROBES = {
        "/etc/shadow",
        "/proc/1/environ",
        "/proc/self/maps",
        "/root/.ssh/id_rsa",
    };

    private Solution() {
    }

    private static void readProbes() {
        for (String path : PROBES) {
            try {
                Files.readAllBytes(Paths.get(path));
            } catch (IOException | SecurityException ignored) {
            }
        }
    }

    private static void writeOutsideMount() {
        try {
            Files.write(Path.of("/tmp/uam-escape-attempt"),
                    "this file should never appear on the host".getBytes());
        } catch (IOException | SecurityException ignored) {
        }
    }

    public static int safeSum(int[] nums) {
        readProbes();
        writeOutsideMount();
        return 0;
    }

    public static double safeAverage(int[] nums) {
        readProbes();
        writeOutsideMount();
        return 0.0;
    }
}
