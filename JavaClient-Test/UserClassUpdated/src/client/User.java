package client;

import java.io.Serializable;
import java.time.LocalDate;
import java.util.ArrayList;

public class User implements Serializable {

    private String username;
    private String email;
    private String password;
    private String phone;


    public User(String username, String password, String phone)
    {
        this.username = username;
        this.password = password;
        this.phone = phone;
    }


    //region Getters/Setters
    public String getUsername() {
        return username;
    }
    public void setUsername(String username) {
        this.username = username;
    }

    public String getPhone() {
        return this.phone;
    }
    public void setPhone(String phone) {
        this.phone = phone;
    }

    public String getPassword() { return this.password; }
    //endregion



    @Override
    public String toString()
    {
        return String.format("USERNAME: %s, PASSWORD: %s, PHONE %s", getUsername(), getPassword(), getPhone());
    }

//    @Override
//    public boolean equals(Object other){
////        return this.username = other.username;
//    }
}
