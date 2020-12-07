package client;

import javafx.beans.value.ChangeListener;
import javafx.beans.value.ObservableValue;
import javafx.collections.FXCollections;
import javafx.event.ActionEvent;
import javafx.event.Event;
import javafx.scene.control.*;

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
    public TextField txtUsernameField;
    public Button btnSendMessage;
    public Button btnLogin;
    public TextField txtRecipName;
    public TextField txtSentMessage;
    public ListView<String> lstReceivedMsg;
    public Tab tabReceivedMessages;
    //endregion

    //region General

    public void initialize(){
        this.lstReceivedMsg = new ListView<>();
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
        if(txtRecipName.getText() != null &&  txtSentMessage.getText() != null){
            String response = Main.client.sendMessageToUser(txtUsernameField.getText(),txtSentMessage.getText());
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
                    txtSentMessage.clear();
                    break;
            }
        }
        else{
            Alert alert = new Alert(Alert.AlertType.ERROR, "Fill out all required fields");
            alert.show();
        }
    }

    public void loadViews(Event event){
        try {
            if (this.tabReceivedMessages.isSelected()) {
                lstReceivedMsg.setItems(FXCollections.observableArrayList(Main.client.printReceived()));
                lstReceivedMsg.refresh();
            }
        }
        catch (NullPointerException ignored){

        }

    }

    //end region
}
