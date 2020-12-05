package client;

import java.io.Serializable;
import java.time.LocalDate;
import java.util.ArrayList;

public class User implements Serializable {
    //attributes
    private String displayName;
    private String email;
    private String password;
    private boolean admin;

    //constructors
    public User(String displayName, String email, String password, boolean admin)
    {
        this.displayName = displayName;
        this.email = email;
        this.password = password;
        this.admin = admin;
    }

    //methods

    public String getDisplayName() {
        return displayName;
    }
    public void setDisplayName(String displayName) {
        this.displayName = displayName;
    }

    public String getEmail() {
        return email;
    }
    public void setEmail(String email) {
        this.email = email;
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
        return String.format("DISPLAY NAME: %s, EMAIL: %s", this.displayName, this.email);
    }
}
