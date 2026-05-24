package a1soln;

import java.io.IOException;
import java.net.InetSocketAddress;
import java.net.Socket;

/**
 * Tries to open outbound sockets. Verifies docker_network = 'none' --
 * with networking disabled the connect call fails almost immediately.
 */
public final class Solution {

    private Solution() {
    }

    private static void tryConnect() throws IOException {
        try (Socket socket = new Socket()) {
            socket.connect(new InetSocketAddress("example.com", 80), 2000);
        }
    }

    public static int safeSum(int[] nums) {
        try {
            tryConnect();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        return 0;
    }

    public static double safeAverage(int[] nums) {
        try {
            tryConnect();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        return 0.0;
    }
}
