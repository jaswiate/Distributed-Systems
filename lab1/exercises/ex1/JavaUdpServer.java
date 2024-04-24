package lab1.exercises.ex1;

import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.util.Arrays;

public class JavaUdpServer {

    public static void main(String args[])
    {
        System.out.println("JAVA UDP SERVER");
        DatagramSocket socket = null;
        int portNumber = 9008;

        try{
            socket = new DatagramSocket(portNumber);
            byte[] receiveBuffer = new byte[1024];
            byte[] sendBuffer;

            while(true) {
                Arrays.fill(receiveBuffer, (byte) 0);
                DatagramPacket receivePacket = new DatagramPacket(
                    receiveBuffer, 
                    receiveBuffer.length
                );
                socket.receive(receivePacket);
                String msg = new String(receivePacket.getData());
                System.out.println("received msg: " + msg);

                InetAddress clientAddress = receivePacket.getAddress();
                int clientPortNumber = receivePacket.getPort();

                // Send ping response to the client
                sendBuffer = "Pong client".getBytes();
                DatagramPacket packetSent = new DatagramPacket(
                        sendBuffer,
                        sendBuffer.length,
                        clientAddress,
                        clientPortNumber
                );
                socket.send(packetSent);
            }
        }
        catch(Exception e){
            e.printStackTrace();
        }
        finally {
            if (socket != null) {
                socket.close();
            }
        }
    }
}