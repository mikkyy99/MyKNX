import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.channels.SocketChannel;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

public class Actor {
    private String address;
    private WriteFunction write;
    private int state;

    public Actor(String address, WriteFunction write) {
        this.address = address;
        this.write = write;
        this.state = 0;
    }

    public void toggle() {
        int newState = (state == 0) ? 1 : 0;
        System.out.println("Sending value: " + newState + " to address: " + address);
        write.write(address, newState);
    }

    public void send(Telegram telegram) {
        if (!telegram.getDst().equals(address)) {
            return;
        }
        if (!(telegram.getValue() instanceof Integer)) {
            return;
        }
        int value = (int) telegram.getValue();
        if (value < 0) {
            return;
        }
        System.out.println("New state of Actor " + address + " is " + value);
        this.state = value;
    }

    @Override
    public String toString() {
        return "Actor<" + address + ">";
    }

    public static void main(String[] args) throws IOException {
        if (args.length != 2) {
            System.err.println("Usage: java Actor <host> <actor address>");
            System.exit(1);
        }

        String host = args[0];
        String actorAddress = args[1];
        String[] hostParts = host.split(":");
        String hostname = hostParts[0];
        int port = (hostParts.length > 1) ? Integer.parseInt(hostParts[1]) : 6720;

        System.out.println("Creating connection to " + hostname + ":" + port);

        try (SocketChannel socketChannel = SocketChannel.open(new InetSocketAddress(hostname, port))) {
            Actor actor = new Actor(actorAddress, new WriteFunction(socketChannel));
            ScheduledExecutorService executorService = Executors.newScheduledThreadPool(1);
            Runtime.getRuntime().addShutdownHook(new Thread(() -> {
                System.out.println("Byte");
                executorService.shutdown();
            }));

            executorService.scheduleAtFixedRate(actor::toggle, 0, 10, TimeUnit.SECONDS);
        }
    }
}

interface WriteFunction {
    void write(String address, int value);
}

class Telegram {
    private String dst;
    private Object value;

    // Getters, setters, and other necessary methods

    public String getDst() {
        return dst;
    }

    public Object getValue() {
        return value;
    }
}
