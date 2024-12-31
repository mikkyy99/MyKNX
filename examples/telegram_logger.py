import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.channels.SocketChannel;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;

public class TelegramLogger {
    public static void main(String[] args) throws IOException {
        if (args.length < 1) {
            System.err.println("Usage: java TelegramLogger <host> [-p port]");
            System.exit(1);
        }

        String host = args[0];
        int port = 6720;
        if (args.length == 3 && args[1].equals("-p")) {
            port = Integer.parseInt(args[2]);
        }

        ScheduledExecutorService executorService = Executors.newScheduledThreadPool(1);

        try (SocketChannel socketChannel = SocketChannel.open(new InetSocketAddress(host, port))) {
            while (true) {
                String line = readLine(socketChannel);
                if (line != null) {
                    System.out.println(line);
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static String readLine(SocketChannel socketChannel) {
        // Implement the logic to read a line from the bus
        return null;
    }
}
