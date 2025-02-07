import java.net.*;
import java.io.*;
import java.util.Scanner;

public class ClientUDP {
    public static void main(String[] args) {
        try {

            DatagramSocket socket = new DatagramSocket();
            InetAddress serverAddress = InetAddress.getByName("192.168.43.49");
            int serverPort = 12345;


            String initialMessage = "Hello Server, I am ready!";

            byte[] message2 = initialMessage.getBytes();
            DatagramPacket sendPacket = new DatagramPacket(message2, message2.length, serverAddress, serverPort);
            socket.send(sendPacket);

            Scanner forServer = new Scanner(System.in);
            System.out.print("Enter your message to the server: ");
            String userInput = forServer.nextLine();

// Convert the user's input into bytes
            byte[] message = userInput.getBytes();


            byte[] receiveBuffer = new byte[1024];

            DatagramPacket receivePacket = new DatagramPacket(receiveBuffer, receiveBuffer.length);
            socket.receive(receivePacket);
            String str = new String(receivePacket.getData(), 0, receivePacket.getLength());
            System.out.println(str);

            // Second receive - expecting message about player selection
            receivePacket = new DatagramPacket(receiveBuffer, receiveBuffer.length);
            socket.receive(receivePacket);
            str = new String(receivePacket.getData(), 0, receivePacket.getLength());
            System.out.println(str);

            // Third receive - expecting Pokémon choice prompt
            receivePacket = new DatagramPacket(receiveBuffer, receiveBuffer.length);
            socket.receive(receivePacket);
            str = new String(receivePacket.getData(), 0, receivePacket.getLength());
            System.out.println(str);

            // Sending Pokémon choice
            System.out.println("Enter your Pokémon choice:");
            int data = forServer.nextInt();
            byte[] sendBuffer = Integer.toString(data).getBytes();

            //socket.send(sendPacket);

            // Fourth receive - expecting confirmation of Pokémon choice
            receivePacket = new DatagramPacket(receiveBuffer, receiveBuffer.length);
            socket.receive(receivePacket);
            str = new String(receivePacket.getData(), 0, receivePacket.getLength());
            System.out.println(str);

            // Fifth receive - message that player 2 is choosing a Pokémon
            receivePacket = new DatagramPacket(receiveBuffer, receiveBuffer.length);
            socket.receive(receivePacket);
            str = new String(receivePacket.getData(), 0, receivePacket.getLength());
            System.out.println(str);

            // Loop for sending and receiving attacks
            for (int i = 0; i <= 100; i++) {
                System.out.println("Enter your attack choice:");
                data = forServer.nextInt();
                sendBuffer = Integer.toString(data).getBytes();
                sendPacket = new DatagramPacket(sendBuffer, sendBuffer.length, serverAddress, serverPort);
                socket.send(sendPacket);

                // Receive attack responses in sequence (expecting 8 messages)
                for (int j = 0; j < 8; j++) {
                    receivePacket = new DatagramPacket(receiveBuffer, receiveBuffer.length);
                    socket.receive(receivePacket);
                    str = new String(receivePacket.getData(), 0, receivePacket.getLength());
                    System.out.println(str);
                }
            }

            // Close the socket
            socket.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}

