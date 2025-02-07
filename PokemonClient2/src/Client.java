import java.net.*;
import java.io.*;
import java.util.Scanner;

public class Client {
    public static void main(String[] args) {
        try {
            // Connect to the server
            Socket s = new Socket("192.168.235.49", 12345);

            PrintWriter pr = new PrintWriter(s.getOutputStream(), true); // pt trimis text
            Scanner forserver = new Scanner(System.in);
            InputStreamReader in = new InputStreamReader(s.getInputStream());
            BufferedReader bf = new BufferedReader(in);  // pt primit text


            String str = bf.readLine();
            System.out.println(str);
            //Player 1 selecting a pokemon

            str = bf.readLine();
            System.out.println(str);
            str = bf.readLine();
            System.out.println(str);
            str = bf.readLine();
            System.out.println(str); //lista de pokemoni plus cerere

            OutputStream out = s.getOutputStream();
            DataOutputStream dos = new DataOutputStream(out);  //output stream este unde trimit chestii

            int data=forserver.nextInt();
            dos.writeInt(data);
            dos.flush(); //aleg pokemon

            str = bf.readLine(); //citesc pokemon
            System.out.println(str); //you chose the second pokemon type shit

            for(int i=0; i<=100; i++){
                str = bf.readLine();
                System.out.println(str);
                str = bf.readLine();
                System.out.println(str);
                str = bf.readLine();
                System.out.println(str);
                str = bf.readLine();
                System.out.println(str);
                data=forserver.nextInt();
                dos.writeInt(data);
                dos.flush();
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
