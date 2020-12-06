package client;

import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;

public class ServerWorker implements Runnable {

    private ServerSocket serverSocket;
    private Socket serverConnection;
    private int port;
    private boolean keepRunningClient;
    private ArrayList<String> incomingMessages;
    private DataOutputStream outputStream;
    private DataInputStream inputStream;

    public ServerWorker (int portToListen){
        this.port = portToListen;
        this.serverSocket = null;
        this.keepRunningClient = true;
        this.incomingMessages = new ArrayList<>();
        this.serverConnection = null;
    }

    //region getters/setters

    public int getPort(){return this.port;}
    public void setPort(int port){this.port = port;}

    public boolean getKeepRunningClient(){return this.keepRunningClient;}
    public void setKeepRunningClient(Boolean state){this.keepRunningClient = state;}


    //endregion

    //region Methods
    @Override
    public void run() {
        this.displayMessage("Connected to Client. Attempting connection to client background thread");
        try {
            this.serverSocket = new ServerSocket(this.port);
            this.serverConnection = serverSocket.accept();
            this.outputStream = new DataOutputStream(serverConnection.getOutputStream());
            this.inputStream = new DataInputStream(serverConnection.getInputStream());

            while (keepRunningClient = true) {
                this.processServerRequest();
            }
        }
        catch(IOException ioe){
                ioe.printStackTrace();
        }
    }

    private void processServerRequest() throws IOException{
        String serverMessage = this.inputStream.readLine();
        displayMessage(String.format("Server said >>>%s", serverMessage));

        String[] arguments = serverMessage.split("\\|");
        String response = "";

        switch (arguments[0]){
            case "R":
                response = String.format("0|%s", arguments[2]);
                String message = arguments[3];
                this.incomingMessages.add(String.format("%s said:%s", arguments[1], message));
                break;
            case "OK":
                response = "0|OK";
                displayMessage(String.format("Message %s successfully received by %s", arguments[3], arguments[2]));
            case "OUT":
                this.terminateConnection();
        }
    }

    private void terminateConnection() {
        this.keepRunningClient = false;
    }

//    public void sendMessage(String msg){
//        this.displayMessage("SEND (BG)>> " + msg);
//        this.serverSocket
//    }

    public String displayMessage(String msg){
        return "SW >> " + msg;
    }
    //endregion



}
