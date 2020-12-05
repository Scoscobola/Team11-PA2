package client;

import java.io.*;
import java.net.Socket;
import java.util.ArrayList;

public class Client {


    private int serverPort;
    private int serverConnectionPort;
    private String serverIP;
    private boolean isConnected;
    private Socket serverConnection;

    private ObjectOutputStream objectOutputStream = null;
    private ObjectInputStream objectInputStream = null;
    private User user;

    public Client ()
    {
        this.serverIP = "localhost";
        this.serverPort = 10001;
        this.serverConnectionPort = 20;
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
            //this.output = this.getOutputStream();
            //this.input = this.getInputStream();
            this.objectOutputStream = new ObjectOutputStream(serverConnection.getOutputStream());
            this.objectInputStream = new ObjectInputStream(serverConnection.getInputStream());
        }
        catch (IOException e)
        {
            //this.input = null;
            //this.output = null;
            this.serverConnection = null;
            this.isConnected = false;
            this.objectOutputStream = null;
            this.objectInputStream = null;
            e.printStackTrace();
        }
    }





    public Object sendRequest (Object request) throws IOException, ClassNotFoundException {
        //this.output.println(request);
        this.objectOutputStream.writeUnshared(request);
        objectOutputStream.flush();
        objectOutputStream.reset();
        displayMessage("CLIENT >> " + request);
        //String srvResponse = this.input.readLine();
        Object srvResponse = this.objectInputStream.readUnshared();
        displayMessage("SERVER >> " + srvResponse);
        return srvResponse;
    }

    public boolean loginUser (String username, String password)
    {
        String request = String.format("L|%s|%s", username, password);
        Request request1 = new Request(request);
        User response = null;
        boolean success = false;
        try
        {
            response = (User) sendRequest(request1);
            if (response != null)
            {
                if (response.isAdmin()) {
                    this.user = response;
                    return success = true;
                }
            }
        }
        catch (IOException | ClassNotFoundException ioe)
        {
            ioe.printStackTrace();
        }
        return success;
    }

    public boolean createNewUser (String displayName, String email, String password, boolean admin)
    {
        boolean success = false;

        if (this.user.isAdmin())
        {
            Request request = new Request(String.format("CU|%s|%s|%s|%s", displayName, email, password, admin));
            String response = null;

            try {
                response = (String) this.sendRequest(request);
            } catch (IOException | ClassNotFoundException ioe) {
                ioe.printStackTrace();
            }

            if (response.contains("Success"))
                success = true;
            else
                success = false;
        }
        return success;
    }

    public ArrayList<User> fetchUsers ()
    {
        ArrayList<User> users = null;
        Request request = new Request("FU");
        //String request = "FU";

        try
        {
            users = (ArrayList<User>)this.sendRequest(request);
        }
        catch(IOException | ClassNotFoundException ioe)
        {
            ioe.printStackTrace();
        }

        return users;
    }


    public boolean saveApp() {
        boolean saved = false;
        Request request = new Request();

        if (this.user.isAdmin())
        {
            String action = "SA|";
            request.setAction(action);
            boolean response = false;

            try
            {
                response = (boolean) this.sendRequest(request);
            }
            catch (IOException | ClassNotFoundException e)
            {
                e.printStackTrace();
            }

            if (response)
                saved = true;
        }
        return saved;
    }
}
