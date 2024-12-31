import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.channels.SocketChannel;

public class SyncRead {
    public static void main(String[] args) throws IOException {
        String host = "nuc";
        try (SocketChannel socketChannel = SocketChannel.open(new InetSocketAddress(host, 6720))) {
            // This only sends a request to the bus which "requests" the current state
            // The response from the bus is sent asynchronously and a bus_monitor/listener
            // has to be used to retrieve the actual state.

            // See examples/actor.py for an example which does that.
            write(socketChannel, "0/0/20");
        }
    }

    private static void write(SocketChannel socketChannel, String address) {
        // Implement the write logic to send the request to the bus
    }
}
