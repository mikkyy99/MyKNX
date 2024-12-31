import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.*;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
public class KnxTest {

    @Test
    public void testEncodeGa() {
        int x = KNX.encodeGA("0/1/14");
        assertEquals(270, x);
    }

    @Test
    public void testDecodeGa() {
        String x = KNX.decodeGA(270);
        assertEquals("0/1/14", x);
    }

    @Test
    public void testEncodeData() {
        byte[] d = KNX.encodeData("HHB", 27, 1, 0);
        assertEquals(new byte[]{0x00, 0x05, 0x00, 0x1b, 0x00, 0x01, 0x00}, d);
    }

    @Test
    public void testTelegramDecoderReceivingSingleBytes() {
        byte[] data = new byte[]{
            0x00, 0x08, 0x00, 0x27, 0x11, (byte) 0xFE, 0x00, 0x07, 0x00, (byte) 0x83
        };
        Telegram telegram = KNX.decodeTelegram(data);
        assertEquals("1.1.254", telegram.getSrc());
        assertEquals("0/0/7", telegram.getDst());
        assertEquals(3, telegram.getValue());
    }

    @Test
    public void testCallWriteWithStrAddr(@Mock SocketChannel writer) throws IOException {
        KNX.write(writer, "0/0/20", 1);
        verify(writer).write(ByteBuffer.wrap(new byte[]{0x00, 0x06, 0x00, 0x27, 0x00, 0x14, 0x00, (byte) 0x81}));
    }

    @Test
    public void testCallWriteWithGaAddr(@Mock SocketChannel writer) throws IOException {
        KNX.write(writer, new GroupAddress(0, 0, 20), 1);
        verify(writer).write(ByteBuffer.wrap(new byte[]{0x00, 0x06, 0x00, 0x27, 0x00, 0x14, 0x00, (byte) 0x81}));
    }

    @Test
    public void testCallRead(@Mock SocketChannel writer) throws IOException {
        KNX.read(writer, new GroupAddress(0, 0, 20));
        verify(writer).write(ByteBuffer.wrap(new byte[]{0x00, 0x06, 0x00, 0x27, 0x00, 0x14, 0x00, 0x00}));
    }

    @Test
    public void testConnectConnectsToSocket(@Mock Socket socket, @Mock SocketChannel socketChannel) throws IOException {
        when(socket.getChannel()).thenReturn(socketChannel);
        try (KNX.Connection conn = new KNX.Connection("localhost", 6720, socket)) {
            verify(socket).connect(new InetSocketAddress("localhost", 6720));
            verify(socketChannel).write(ByteBuffer.wrap(new byte[]{0x00, 0x05, 0x00, 0x26, 0x00, 0x00, 0x00}));
        } catch (Exception e) {
            e.printStackTrace();
        }
        verify(socket).close();
    }
}
