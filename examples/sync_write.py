import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.channels.SocketChannel;

public class SyncWrite {
    public static void main(String[] args) throws IOException {
        String host = "nuc";
        try (SocketChannel socketChannel = SocketChannel.open(new InetSocketAddress(host, 6720))) {
            write(socketChannel, "0/0/20", 1);
        }
    }

    private static void write(SocketChannel socketChannel, String address, int value) {
        // Implement the write logic to send the command to the bus
    }
}
