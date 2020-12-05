package client;

import java.io.Serializable;

public class Request implements Serializable
{
    private String action;
    private Object message;

    public Request ()
    {
        this.action = null;
        this.message = null;
    }

    public Request(String action)
    {
        this.action = action;
        this.message = null;
    }

    public Request (String action, Object message)
    {
        this.action = action;
        this.message = message;
    }

    public String getAction(){return this.action;}
    public void setAction(String action){this.action = action;}

    public Object getMessage(){return this.message;}
    public void setMessage(Object message){this.message = message;}





}