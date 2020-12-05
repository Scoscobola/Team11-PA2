package client;

import java.io.*;
import java.net.Socket;
import java.util.ArrayList;

public class BackgroundClientWorker implements Runnable {

    private Thread thread;
    private int id;
    private Socket clientSocket;
    private Socket serverSocket;
    //private Database database;
    private int port;
    private User user;
    private boolean keepRunningClient;

    //region getters/setters
    public int getID(){return this.id;}
    public void setID(int clientId){this.id = clientId;}

    public Socket getClientSocket(){return this.clientSocket;}
    public void setClientSocket(Socket socket){this.clientSocket = socket;}

    ///  public Database getDatabase(){return this.database}
    ///  public void setDatabase(Database db){this.database = db}

    public int getPort(){return this.port;}
    public void setPort(int port){this.port = port;}

    public User getUser(){return this.user;}
    public void setUser(User user){this.user = user;}

    public boolean getKeepRunningClient(){return this.keepRunningClient;}
    public void setKeepRunningClient(Boolean state){this.keepRunningClient = state;}


    //endregion

    //region Methods
    @Override
    public void run() {
        this.displayMessage("Connected to Client. Attempting connection to client background thread");
//        while (keepRunningClient = true){
//            try {
//                this.serverSocket = serverSocket()
//            }
//            catch ()
//
//        }


    }

//    public void sendMessage(String msg){
//        this.displayMessage("SEND (BG)>> " + msg);
//        this.serverSocket.send(msg.encode("UTF-16"))
//    }

    public String displayMessage(String msg){
        return "BGCW >> " + msg;
    }
    //endregion



}
