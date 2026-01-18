package com.news_ai.stock.ui.layout;

import javafx.geometry.Pos;
import javafx.scene.Node;
import javafx.scene.layout.HBox;
import javafx.scene.layout.Priority;
import javafx.scene.layout.VBox;

public class CenteredContentPane extends HBox {

    private final VBox content;

    public CenteredContentPane(double maxContentWidth, double spacing) {
        setAlignment(Pos.TOP_CENTER);
        setFillHeight(true);
        HBox.setHgrow(this, Priority.ALWAYS);

        content = new VBox(spacing);
        content.setMaxWidth(maxContentWidth);
        content.setFillWidth(true);

        getChildren().add(content);
    }

    public VBox getContent() {
        return content;
    }

    public void add(Node node) {
        content.getChildren().add(node);
    }
}
