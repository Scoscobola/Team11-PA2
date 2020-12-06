package client;

import java.io.Serializable;
import java.time.LocalDate;
import java.util.ArrayList;

public class User implements Serializable {
    //attributes
    private String displayName;
    private int phone;
    private String password;
    private boolean admin;

    //constructors
    public User(String displayName, String password, int phone)
    {
        this.displayName = displayName;
        this.password = password;
        this.phone = phone;
    }

    //methods

    public String getDisplayName() {
        return displayName;
    }
    public void setDisplayName(String displayName) {
        this.displayName = displayName;
    }

    public int getPhone() {
        return phone;
    }
    public void setEmail(int phone) {
        this.phone = phone;
    }

    public void setPassword(String password) {
        this.password = password;
    }
    public String getPassword() {return this.password;}

    public boolean isAdmin() {
        return admin;
    }
    public void setAdmin(boolean admin) {
        this.admin = admin;
    }


    @Override
    public String toString()
    {
        return String.format("DISPLAY NAME: %s, PHONE: %s", this.displayName, this.phone);
    }
}
