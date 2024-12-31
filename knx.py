import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.ByteBuffer;
import java.nio.channels.SocketChannel;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.function.Consumer;

public class KNX {
    private static final int EIB_OPEN_GROUPCON = 0x26;
    private static final int EIB_GROUP_PACKET = 0x27;
    private static final int KNXWRITE = 0x80;
    private static final int KNXREAD = 0x00;

    public static int encodeGA(String addr) {
        String[] parts = addr.split("/");
        return (Integer.parseInt(parts[0]) << 11) + (Integer.parseInt(parts[1]) << 8) + Integer.parseInt(parts[2]);
    }

    public static String decodeIA(int ia) {
        return String.format("%d.%d.%d", (ia >> 12) & 0x1f, (ia >> 8) & 0x07, ia & 0xff);
    }

    public static String decodeGA(int ga) {
        return String.format("%d/%d/%d", (ga >> 11) & 0x1f, (ga >> 8) & 0x07, ga & 0xff);
    }

    public static byte[] encodeData(String fmt, Object... data) {
        ByteBuffer buffer = ByteBuffer.allocate(65536);
        buffer.putShort((short) (data.length * 2));
        for (Object d : data) {
            if (d instanceof Integer) {
                buffer.putInt((Integer) d);
            } else if (d instanceof Byte) {
                buffer.put((Byte) d);
            }
        }
        return buffer.array();
    }

    public static void write(SocketChannel socketChannel, String addr, int value) throws IOException {
        int encodedAddr = encodeGA(addr);
        byte[] data = encodeData("HHBB", EIB_GROUP_PACKET, encodedAddr, 0, KNXWRITE | value);
        socketChannel.write(ByteBuffer.wrap(data));
    }

    public static void read(SocketChannel socketChannel, String addr) throws IOException {
        int encodedAddr = encodeGA(addr);
        byte[] data = encodeData("HHBB", EIB_GROUP_PACKET, encodedAddr, 0, KNXREAD);
        socketChannel.write(ByteBuffer.wrap(data));
    }

    public static void main(String[] args) throws IOException {
        if (args.length != 2) {
            System.err.println("Usage: java KNX <host> <actor address>");
            System.exit(1);
        }

        String host = args[0];
        String actorAddress = args[1];
        String[] hostParts = host.split(":");
        String hostname = hostParts[0];
        int port = (hostParts.length > 1) ? Integer.parseInt(hostParts[1]) : 6720;

        System.out.println("Creating connection to " + hostname + ":" + port);

        try (SocketChannel socketChannel = SocketChannel.open(new InetSocketAddress(hostname, port))) {
            write(socketChannel, actorAddress, 1);
            read(socketChannel, actorAddress);
        }
    }
}
