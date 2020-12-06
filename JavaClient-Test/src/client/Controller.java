package client;

import javafx.event.ActionEvent;
import javafx.scene.control.Alert;
import javafx.scene.control.Button;
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
    public Button btnLogin;
    //endregion

    //region General

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

    public void connectToApp(ActionEvent actionEvent) {
    }

    //end region
}
