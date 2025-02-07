import java.net.*;
import java.io.*;
import java.util.Scanner;

public class Client {
    public static void main(String[] args) {
        try {
            // Connect to the server
            Socket s = new Socket("192.168.235.49", 12345);
            //Socket s = new Socket("127.0.0.1", 12345);

            // Send data to the server
            PrintWriter pr = new PrintWriter(s.getOutputStream(), true); // pt trimis text
            Scanner forserver=new Scanner(System.in);
            //pr.println(data);

            // Receive response from the server
            InputStreamReader in = new InputStreamReader(s.getInputStream());
            BufferedReader bf = new BufferedReader(in);  // pt primit text
            OutputStream out = s.getOutputStream();
            DataOutputStream dos = new DataOutputStream(out);  //output stream este unde trimit chestii

            String str = bf.readLine();
            System.out.println(str);
            str = bf.readLine();
            System.out.println(str);
            str = bf.readLine();
            System.out.println(str);
             //please chose your pokemon type shit
            int data=forserver.nextInt();
            dos.writeInt(data);
            dos.flush();  //trimita decizia nenicului


            str = bf.readLine();
            System.out.println(str); //you chose blabla

            str = bf.readLine();
            System.out.println(str); //player 2 alege pokemon

            for(int i=0; i<=100; i++){
                System.out.println("Enter your attack!");
                data=forserver.nextInt();
                dos.writeInt(data);
                dos.flush();
                str = bf.readLine();
                System.out.println(str);
                str = bf.readLine();
                System.out.println(str); //atac
                str = bf.readLine();
                System.out.println(str);
                str = bf.readLine();
                System.out.println(str);
                str = bf.readLine();
                System.out.println(str);
                str = bf.readLine();
                System.out.println(str);
                str = bf.readLine();
                System.out.println(str);

            }

            s.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
