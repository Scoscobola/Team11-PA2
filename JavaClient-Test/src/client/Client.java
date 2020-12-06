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

    public Client() {
        this.serverIP = "localhost";
        this.serverPort = 10001;
        this.serverConnectionPort = 20;
        this.serverWorker = new ServerWorker(20);
        this.isConnected = false;
        this.isLoggedIn = false;
    }


    public int getServerPort() {
        return this.serverPort;
    }

    public void setServerPort(int serverPort) {
        this.serverPort = serverPort;
    }

    public String getServerIP() {
        return this.serverIP;
    }

    public void setServerIP(String ip) {
        this.serverIP = ip;
    }

    public int getServerConnection() {
        return this.serverConnectionPort;
    }

    public void setServerConnection(int serverConnectionPort) {
        this.serverConnectionPort = serverConnectionPort;
    }

    public boolean isConnected() {
        return this.isConnected;
    }

    public boolean isLoggedIn() {
        return this.isLoggedIn;
    }

    private void displayMessage(String message) {
        System.out.println(message);
    }


    public void connect() {
        displayMessage("Attempting connection to Server");

        try {
            this.serverConnection = new Socket(this.serverIP, this.serverPort);
            this.isConnected = true;
            this.outputStream = new DataOutputStream(serverConnection.getOutputStream());
            this.inputStream = new DataInputStream(serverConnection.getInputStream());
            this.serverWorker.setPort(this.serverConnectionPort);
            ExecutorService executorService = Executors.newCachedThreadPool();
            executorService.execute(this.serverWorker);
            this.sendRequest(String.format("PORT|%s", this.serverConnectionPort));
        } catch (IOException e) {
            this.serverConnection = null;
            this.isConnected = false;
            this.outputStream = null;
            this.inputStream = null;
            e.printStackTrace();
        }
    }

    public String disconnect(){
        String result = "";
        if (isConnected){
            try {
                String response = this.sendRequest("OUT|OK");
                String[] arguments = response.split("\\|");
                if (arguments[0].equals("0")){
                    result = String.format("%s|%s", arguments[0], arguments[1]);
                    this.displayMessage(result);
                }
                else if (arguments[0].equals("1")){
                    result = arguments[1];
                    this.displayMessage(arguments[1]);
                }
                this.serverWorker.terminateConnection();
                this.closeConnection();
            }
            catch (IOException ioe){
                ioe.printStackTrace();
            }
        }
        return result;
    }

    private void closeConnection() {
        try{
            this.inputStream.close();
        }
        catch(IOException ioe){
            ioe.printStackTrace();
        }
        try{
            this.outputStream.close();
        }
        catch (IOException ioe){
            ioe.printStackTrace();
        }
        try{
            this.serverConnection.close();
        }
        catch (IOException ioe){
            ioe.printStackTrace();
        }
    }


    public String sendRequest(String request) throws IOException {
        this.outputStream.writeBytes(request + "\n");
        this.outputStream.flush();
        displayMessage("CLIENT >> " + request);
        byte[] bytes = new byte[1024];
        this.inputStream.read(bytes);
        String srvResponse = new String(bytes, StandardCharsets.UTF_8);
        srvResponse = srvResponse.replace("\n", "");
        displayMessage("SERVER >> " + srvResponse);
        return srvResponse;
    }

    public String loginUser(String username, String password) {
        String result = "";
        if (isConnected) {
            String request = String.format("LOG|%s|%s", username, password);
            String response = null;
            try {
                if (isConnected) {
                    response = sendRequest(request);
                    String[] arguments = response.split("\\|");

                    switch (arguments[0]) {
                        case "0":
                            displayMessage("Signed In successfully");
                            result = "0|S";
                            this.username = username;
                            this.isLoggedIn = true;
                            break;
                        case "1":
                            displayMessage("Invalid Credentials");
                            result = "1|I";
                            break;
                        case "2":
                            displayMessage("Already logged in.");
                            result = "2|A";
                            break;
                        default:
                            displayMessage("1|ERR");
                            result = "3|E";
                    }
                } else {
                    displayMessage("The client is not connected to a server!");
                }
            } catch (IOException ioe) {
                ioe.printStackTrace();
            }
        }
        return result;
    }

    public String createNewUser(String displayName, String password, int phone) {
        String result = "";
        if (isConnected) {
            String request = String.format("USR|%s|%s|%s", displayName, password, phone);
            String response = null;
            try {
                response = this.sendRequest(request);
                String[] arguments = response.split("\\|");
                if (arguments[0].equals("0")) {
                    this.displayMessage("User signed up successfully");
                    result = "User signed up successfully";
                } else if (arguments[0].equals("1")) {
                    this.displayMessage(arguments[1]);
                    result = arguments[1];
                }

            } catch (IOException ioe) {
                ioe.printStackTrace();
            }
        }

        return result;
    }

    public String sendMessageToUser(String username, String msg) {
        String result = "";
        if (isConnected && isLoggedIn) {
            try {
                String response = this.sendRequest(String.format("MSG|%s|%s|%s", this.username, username, msg));
                String[] arguments = response.split("\\|");

                switch (arguments[0]) {
                    case "0":
                        result = String.format("Message %s sent successfully.", arguments[1]);
                        this.displayMessage(result);
                        break;
                    case "1":
                        result = "The user sending the message doesn't exist or is not the current user logged in.";
                        this.displayMessage(result);
                        break;
                    case "2":
                        result = "The target user doesn't exist.";
                        this.displayMessage(result);
                        break;
                }
            } catch (IOException ioe) {
                ioe.printStackTrace();
            }
        }
        return result;
    }

    public ArrayList<String> printReceived(){
        if (!this.serverWorker.getIncomingMessages().isEmpty()){
            for (String s: this.serverWorker.getIncomingMessages()){
                displayMessage(s);
            }
        }
        else {
            displayMessage("No new messages.");
        }
        return this.serverWorker.getIncomingMessages();
    }
}
