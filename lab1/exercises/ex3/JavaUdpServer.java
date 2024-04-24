package lab1.exercises.ex3;

import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.util.Arrays;

public class JavaUdpServer {
    public static void main(String[] args) {
        System.out.println("JAVA UDP SERVER");
        DatagramSocket socket = null;
        int portNumber = 9009;

        try {
            socket = new DatagramSocket(portNumber);
            byte[] receiveBuffer = new byte[1024];
            byte[] sendBuffer;

            while (true) {
                Arrays.fill(receiveBuffer, (byte) 0);
                DatagramPacket receivePacket = new DatagramPacket(
                    receiveBuffer, 
                    receiveBuffer.length
                );
                socket.receive(receivePacket);
                int number = ByteBuffer.wrap(receiveBuffer).order(
                    ByteOrder.LITTLE_ENDIAN).getInt();
                System.out.println("received msg: " + number);
                number += 1;

                InetAddress clientAddress = receivePacket.getAddress();
                
                int clientPortNumber = receivePacket.getPort();
                sendBuffer = ByteBuffer.allocate(4).order(
                    ByteOrder.LITTLE_ENDIAN).putInt(number).array();
                DatagramPacket packetSent = new DatagramPacket(
                        sendBuffer,
                        sendBuffer.length,
                        clientAddress,
                        clientPortNumber
                );
                socket.send(packetSent);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
