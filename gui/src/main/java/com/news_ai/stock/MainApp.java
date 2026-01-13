package com.news_ai.stock;

import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.Label;
import javafx.scene.layout.StackPane;
import javafx.stage.Stage;

public class MainApp extends Application {

    @Override
    public void start(Stage stage) {
        String javaVersion = System.getProperty("java.version");
        String javafxVersion = System.getProperty("javafx.version");
        Label l = new Label("Stock News Pro: Java GUI Loading...");
        Scene scene = new Scene(new StackPane(l), 800, 600);
        stage.setScene(scene);
        stage.setTitle("Stock News Pro");
        stage.show();
    }

    public static void main(String[] args) {
        launch();
    }
}
