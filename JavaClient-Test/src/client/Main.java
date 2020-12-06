package client;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Stage;

public class Main extends Application {

    public static ScreenController screenController;
    public static Controller c;
    public static Client client = new Client();
    public static void main(String[] args) {
        launch(args);
    }


    @Override
    public void start(Stage primaryStage) throws Exception{
        FXMLLoader loader = new FXMLLoader(getClass().getResource("clientConnect.fxml"));
        Parent root = loader.load();
        c = loader.getController();
        primaryStage.setTitle("");
        primaryStage.setScene(new Scene(root, 800, 600));
        screenController = new ScreenController(primaryStage.getScene());
        screenController.addScreen("ServerConnect", FXMLLoader.load(getClass().getResource("clientConnect.fxml")));
        screenController.addScreen("ClientLogin", FXMLLoader.load(getClass().getResource("clientLogin.fxml")));
        screenController.addScreen("ClientMenu", FXMLLoader.load(getClass().getResource("clientMenu.fxml")));
        primaryStage.show();
    }
}
