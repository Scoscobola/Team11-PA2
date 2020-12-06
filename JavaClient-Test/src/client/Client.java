package client;

import java.io.*;
import java.net.Socket;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class Client {

    private int serverPort;
    private int serverConnectionPort;
    private String serverIP;
    private boolean isConnected;
    private boolean isLoggedIn;
    private Socket serverConnection;
    private ServerWorker serverWorker;

    private DataOutputStream outputStream = null;
    private DataInputStream inputStream = null;
    private String username;

    public Client ()
    {
        this.serverIP = "localhost";
        this.serverPort = 10001;
        this.serverConnectionPort = 20;
        this.serverWorker = new ServerWorker(20);
        this.isConnected = false;
        this.isLoggedIn = false;
    }



    public int getServerPort(){return this.serverPort;}
    public void setServerPort(int serverPort){this.serverPort = serverPort;}

    public String getServerIP(){return this.serverIP;}
    public void setServerIP(String ip){this.serverIP = ip;}

    public int getServerConnection(){return this.serverConnectionPort;}
    public void setServerConnection(int serverConnectionPort){this.serverConnectionPort = serverConnectionPort;}

    public boolean isConnected() {return this.isConnected;}

    private void displayMessage(String message) {System.out.println(message);}


    public void connect()
    {
        displayMessage ("Attempting connection to Server");
        PrintWriter output = null;
        BufferedReader input = null;

        try
        {
            this.serverConnection = new Socket (this.serverIP, this.serverPort);
            this.isConnected = true;
            this.outputStream = new DataOutputStream(serverConnection.getOutputStream());
            this.inputStream = new DataInputStream(serverConnection.getInputStream());
            ExecutorService executorService = Executors.newCachedThreadPool();
            executorService.execute(this.serverWorker);
            this.sendRequest(String.format("PORT|%s", this.serverConnectionPort));
        }
        catch (IOException e)
        {
            //this.input = null;
            //this.output = null;
            this.serverConnection = null;
            this.isConnected = false;
            this.outputStream = null;
            this.inputStream = null;
            e.printStackTrace();
        }
    }


    public String sendRequest (String request) throws IOException{
        this.outputStream.writeBytes(request);
        this.outputStream.flush();
        displayMessage("CLIENT >> " + request);
        String srvResponse = this.inputStream.readUTF();
        displayMessage("SERVER >> " + srvResponse);
        return srvResponse;
    }

    public boolean loginUser (String username, String password)
    {
        String request = String.format("LOG|%s|%s", username, password);
        String response = null;
        boolean success = false;
        try
        {
            if (isConnected) {
                response = sendRequest(request);
                String[] arguments = response.split("\\|");

                if (arguments[0].equals("0")) {
                    displayMessage("Signed In successfully");
                    this.username = username;
                } else if (arguments[0].equals("1")) {
                    displayMessage("Invalid Credentials");
                } else if (arguments[0].equals("2")) {
                    displayMessage("Already logged in.");
                }
            }
            else{
                displayMessage("The client is not connected to a server!");
            }
        }
        catch (IOException ioe)
        {
            ioe.printStackTrace();
        }
        return success;
    }

//    public boolean createNewUser (String displayName, String email, String password, boolean admin)
//    {
//        boolean success = false;
//
//        if (this.user.isAdmin())
//        {
//            Request request = new Request(String.format("CU|%s|%s|%s|%s", displayName, email, password, admin));
//            String response = null;
//
//            try {
//                response = (String) this.sendRequest(request);
//            } catch (IOException | ClassNotFoundException ioe) {
//                ioe.printStackTrace();
//            }
//
//            if (response.contains("Success"))
//                success = true;
//            else
//                success = false;
//        }
//        return success;
//    }

//    public ArrayList<User> fetchUsers ()
//    {
//        ArrayList<User> users = null;
//        Request request = new Request("FU");
//        //String request = "FU";
//
//        try
//        {
//            users = (ArrayList<User>)this.sendRequest(request);
//        }
//        catch(IOException | ClassNotFoundException ioe)
//        {
//            ioe.printStackTrace();
//        }
//
//        return users;
//    }


//    public boolean saveApp() {
//        boolean saved = false;
//        Request request = new Request();
//
//        if (this.user.isAdmin())
//        {
//            String action = "SA|";
//            request.setAction(action);
//            boolean response = false;
//
//            try
//            {
//                response = (boolean) this.sendRequest(request);
//            }
//            catch (IOException | ClassNotFoundException e)
//            {
//                e.printStackTrace();
//            }
//
//            if (response)
//                saved = true;
//        }
//        return saved;
//    }
}