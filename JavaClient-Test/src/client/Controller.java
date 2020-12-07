package client;

import javafx.event.ActionEvent;
import javafx.scene.control.Alert;
import javafx.scene.control.Button;
import javafx.scene.control.TextArea;
import javafx.scene.control.TextField;

import java.io.IOException;

public class Controller {
    //region Controlls
    public TextField txtIP;
    public TextField txtPort;
    public TextField txtPortServerConnect;
    public Button btnConnect;
    public Button btnExit;
    public TextField txtUser;
    public TextField txtPass;
    public TextArea taComment;
    public TextField tfComment;
    public TextField txtUsernameField;
    public Button btnSendMessage;
    public Button btnLogin;
    //endregion

    //region General

    public void initialize(){
        this.taComment.
    }

    public void changeScene(String fxml) throws IOException {
        Main.screenController.activate(fxml);
    }

    public void exitApp(ActionEvent actionEvent) {
        Runtime.getRuntime().exit(0);
    }


    //endregion


    //region ServerConnection

    public void connectToSrv(ActionEvent actionEvent) throws IOException{
        if (txtIP.getText() != null && txtPort.getText() != null && txtPortServerConnect.getText() != null){
            Main.client.setServerIP(txtIP.getText());
            Main.client.setServerPort(Integer.parseInt(txtPort.getText()));
            Main.client.setServerConnection(Integer.parseInt(txtPortServerConnect.getText()));
            Main.client.connect();

            if(Main.client.isConnected()){
                changeScene("ClientLogin");
            }
            else {
                Alert alert = new Alert(Alert.AlertType.ERROR, "Could not connect to server. Check your data values and try again.");
                txtPortServerConnect.clear();
                txtPort.clear();
                txtIP.clear();
                alert.show();
            }
        }
        else {
            Alert alert = new Alert(Alert.AlertType.ERROR, "Fill out all required fields");
            alert.show();
        }
    }

    //endregion



    //region ConnectToMsgApp

    public void connectToApp(ActionEvent actionEvent) throws IOException{
        String status = null;
        String[] arguments = null;
        if(txtUser.getText() != null && txtPass.getText() != null){
            status = Main.client.loginUser(txtUser.getText(), txtPass.getText());
            arguments = status.split("\\|");
            if(Main.client.isLoggedIn()){
               changeScene("ClientMenu");
            }
            else{
                switch (arguments[0]){
                    case "0":
                        Alert alert = new Alert(Alert.AlertType.CONFIRMATION, arguments[1]);
                        alert.show();
                        break;
                    case "1":
                    case "2":
                    case "3":
                        Alert error = new Alert(Alert.AlertType.ERROR, arguments[1]);
                        error.show();
                        txtUser.clear();
                        txtPass.clear();
                        //changeScene("ClientLogin");
                        break;

                }
            }
        }
        else{
            Alert alert = new Alert(Alert.AlertType.ERROR, "Fill out all required fields");
            alert.show();
        }

    }

    public void sendMessage(ActionEvent actionEvent)throws IOException{
        if(txtUsernameField.getText() != null &&  tfComment.getText() != null){
            String response = Main.client.sendMessageToUser(txtUsernameField.getText(),tfComment.getText());
            taComment.appendText(String.format("%s: %s",txtUser.getText() , tfComment.getText()));
            String[] arguments = response.split("\\|");
            switch (arguments[0]){
                case "0":
                    Alert alert = new Alert(Alert.AlertType.CONFIRMATION, arguments[1]);
                    alert.show();
                    break;
                case "1":
                case "2":
                    Alert error = new Alert(Alert.AlertType.ERROR, arguments[1]);
                    error.show();
                    txtUsernameField.clear();
                    tfComment.clear();
                    break;
            }
        }
        else{
            Alert alert = new Alert(Alert.AlertType.ERROR, "Fill out all required fields");
            alert.show();
        }
    }

    //end region
}
