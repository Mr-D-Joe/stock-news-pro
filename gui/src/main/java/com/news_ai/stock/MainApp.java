package com.news_ai.stock;

import com.news_ai.stock.viewmodel.MainViewModel;
import javafx.application.Application;
import javafx.application.Platform;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.layout.*;
import javafx.stage.Stage;
import javafx.beans.property.StringProperty;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.scene.input.Clipboard;
import javafx.scene.input.ClipboardContent;

/**
 * Stock News Pro - Modern Dashboard UI
 * 
 * Clean, professional interface matching the DeltaValue design language.
 * Features: Ticker input, Sector dropdown, Language selection, Report
 * generation.
 */
public class MainApp extends Application {

    private MainViewModel viewModel;

    @Override
    public void start(Stage stage) {
        viewModel = new MainViewModel();

        // Main layout
        BorderPane root = new BorderPane();
        root.getStyleClass().add("root");

        // Top: Clean input bar
        HBox topBar = createTopBar();
        root.setTop(topBar);

        // Center: Dashboard cards
        HBox dashboard = createDashboard();
        root.setCenter(dashboard);

        // Bottom: Minimal status bar
        HBox statusBar = createStatusBar();
        root.setBottom(statusBar);

        // Scene setup
        Scene scene = new Scene(root, 1100, 700);
        scene.getStylesheets().add(getClass().getResource("/styles/main.css") != null
                ? getClass().getResource("/styles/main.css").toExternalForm()
                : "");

        stage.setScene(scene);
        stage.setTitle("Stock News Pro");
        stage.setOnCloseRequest(e -> {
            Platform.exit();
            System.exit(0);
        });
        stage.show();

        // Auto-connect on startup
        viewModel.checkConnection();
    }

    private HBox createTopBar() {
        HBox bar = new HBox(20);
        bar.setPadding(new Insets(16, 24, 16, 24));
        bar.setAlignment(Pos.CENTER_LEFT);
        bar.setStyle("-fx-background-color: white; -fx-border-color: #e5e5ea; -fx-border-width: 0 0 1 0;");

        double inputWidth = 180;
        double inputHeight = 36;
        String inputStyle = "-fx-background-color: white; -fx-border-color: #d2d2d7; -fx-border-radius: 6; -fx-background-radius: 6;";

        // Ticker input with label
        VBox tickerBox = new VBox(4);
        tickerBox.setAlignment(Pos.CENTER_LEFT);
        Label tickerLabel = new Label("Aktie");
        tickerLabel.setStyle("-fx-text-fill: #86868b; -fx-font-size: 11px; -fx-font-weight: 600;");
        TextField tickerField = new TextField();
        tickerField.setPromptText("z.B. NVO, GOOG, TSLA...");
        tickerField.setPrefWidth(inputWidth);
        tickerField.setPrefHeight(inputHeight);
        tickerField.setStyle(inputStyle);
        tickerField.textProperty().bindBidirectional(viewModel.selectedTickerProperty());
        tickerField.focusedProperty().addListener((obs, old, focused) -> {
            if (!focused)
                viewModel.resolveTicker();
        });
        tickerField.setOnAction(e -> viewModel.exportHtmlReport());
        tickerBox.getChildren().addAll(tickerLabel, tickerField);

        // Sector dropdown with label - editable ComboBox (styling via CSS)
        VBox sectorBox = new VBox(4);
        sectorBox.setAlignment(Pos.CENTER_LEFT);
        Label sectorLabel = new Label("Branche");
        sectorLabel.setStyle("-fx-text-fill: #86868b; -fx-font-size: 11px; -fx-font-weight: 600;");
        ComboBox<String> sectorCombo = new ComboBox<>();
        sectorCombo.setPromptText("Optional...");
        sectorCombo.setPrefWidth(inputWidth);
        sectorCombo.setPrefHeight(inputHeight);
        sectorCombo.getItems().addAll("Technology", "Healthcare", "Finance", "Automotive", "Energy", "Consumer",
                "Industrial", "Real Estate", "Biotechnology", "Pharmaceuticals");
        sectorCombo.setEditable(true);
        // Manual binding to force update
        if (viewModel.getSelectedSector() != null)
            sectorCombo.getEditor().setText(viewModel.getSelectedSector());
        sectorCombo.getEditor().textProperty().addListener((obs, o, n) -> viewModel.setSelectedSector(n));
        viewModel.selectedSectorProperty().addListener((obs, o, n) -> {
            if (n != null && !n.equals(sectorCombo.getEditor().getText())) {
                sectorCombo.getEditor().setText(n);
            }
        });
        sectorBox.getChildren().addAll(sectorLabel, sectorCombo);

        // Language dropdown with label - editable ComboBox (styling via CSS)
        VBox langBox = new VBox(4);
        langBox.setAlignment(Pos.CENTER_LEFT);
        Label langLabel = new Label("Sprache");
        langLabel.setStyle("-fx-text-fill: #86868b; -fx-font-size: 11px; -fx-font-weight: 600;");
        ComboBox<String> langCombo = new ComboBox<>();
        langCombo.getItems().addAll(
                "German / Deutsch", "English", "French / Français", "Spanish / Español", "Italian / Italiano",
                "Japanese / 日本語", "Chinese / 中文", "Portuguese / Português", "Russian / Русский",
                "Dutch / Nederlands", "Korean / 한국어", "Polish / Polski", "Turkish / Türkisch", "Arabic / العربية");
        langCombo.setPrefWidth(inputWidth);
        langCombo.setPrefHeight(inputHeight);
        langCombo.setEditable(true);

        // Setup Autocomplete & ViewModel Binding
        setupAutocomplete(langCombo, viewModel.selectedLanguageProperty());

        // Initial value
        if (viewModel.getSelectedLanguage() != null) {
            langCombo.getEditor().setText(viewModel.getSelectedLanguage());
        }

        langBox.getChildren().addAll(langLabel, langCombo);

        Region spacer = new Region();
        HBox.setHgrow(spacer, Priority.ALWAYS);

        ProgressIndicator spinner = new ProgressIndicator();
        spinner.setMaxSize(20, 20);
        spinner.visibleProperty().bind(viewModel.loadingProperty());
        spinner.managedProperty().bind(viewModel.loadingProperty());

        // Analyze button - subtle green outline style
        Button analyzeBtn = new Button("Analyze");
        String analyzeBtnStyle = "-fx-background-color: transparent; -fx-text-fill: #22c55e; -fx-border-color: #22c55e; -fx-border-width: 1.5; -fx-border-radius: 6; -fx-background-radius: 6; -fx-padding: 6 16; -fx-cursor: hand; -fx-font-size: 12px; -fx-font-weight: 500;";
        String analyzeBtnHover = "-fx-background-color: #22c55e; -fx-text-fill: white; -fx-border-color: #22c55e; -fx-border-width: 1.5; -fx-border-radius: 6; -fx-background-radius: 6; -fx-padding: 6 16; -fx-cursor: hand; -fx-font-size: 12px; -fx-font-weight: 500;";
        analyzeBtn.setStyle(analyzeBtnStyle);
        analyzeBtn.setOnMouseEntered(e -> analyzeBtn.setStyle(analyzeBtnHover));
        analyzeBtn.setOnMouseExited(e -> analyzeBtn.setStyle(analyzeBtnStyle));
        analyzeBtn.setOnAction(e -> viewModel.exportHtmlReport());
        analyzeBtn.disableProperty().bind(viewModel.loadingProperty().or(viewModel.connectedProperty().not()));

        // Exit button - subtle red outline style
        Button exitBtn = new Button("Exit");
        String exitBtnStyle = "-fx-background-color: transparent; -fx-text-fill: #ef4444; -fx-border-color: #ef4444; -fx-border-width: 1.5; -fx-border-radius: 6; -fx-background-radius: 6; -fx-padding: 6 16; -fx-cursor: hand; -fx-font-size: 12px; -fx-font-weight: 500;";
        String exitBtnHover = "-fx-background-color: #ef4444; -fx-text-fill: white; -fx-border-color: #ef4444; -fx-border-width: 1.5; -fx-border-radius: 6; -fx-background-radius: 6; -fx-padding: 6 16; -fx-cursor: hand; -fx-font-size: 12px; -fx-font-weight: 500;";
        exitBtn.setStyle(exitBtnStyle);
        exitBtn.setOnMouseEntered(e -> exitBtn.setStyle(exitBtnHover));
        exitBtn.setOnMouseExited(e -> exitBtn.setStyle(exitBtnStyle));
        exitBtn.setOnAction(e -> {
            // Kill uvicorn server process before exiting
            try {
                ProcessBuilder pb = new ProcessBuilder("/bin/zsh", "-c", "pkill -f 'uvicorn ai_service.main:app'");
                pb.start();
                Thread.sleep(500);
            } catch (Exception ex) {
                System.err.println("Could not kill server: " + ex.getMessage());
            }
            Platform.exit();
            System.exit(0);
        });

        // Connection dot with Tooltip
        Label connectionDot = new Label("●");
        connectionDot.setStyle("-fx-text-fill: #ef4444; -fx-font-size: 18px; -fx-cursor: hand;");
        Tooltip connectionTooltip = new Tooltip("❌ Disconnected: Checking...");
        connectionTooltip.setStyle("-fx-font-size: 12px;");
        connectionTooltip.setShowDelay(javafx.util.Duration.ZERO);
        connectionTooltip.setHideDelay(javafx.util.Duration.seconds(3));
        Tooltip.install(connectionDot, connectionTooltip);
        viewModel.connectedProperty().addListener((obs, old, connected) -> {
            if (connected) {
                connectionDot.setStyle("-fx-text-fill: #22c55e; -fx-font-size: 18px; -fx-cursor: hand;");
                connectionTooltip.setText("✅ Connected: AI Service running at localhost:8000");
            } else {
                connectionDot.setStyle("-fx-text-fill: #ef4444; -fx-font-size: 18px; -fx-cursor: hand;");
                connectionTooltip.setText(
                        "❌ Disconnected: Cannot reach localhost:8000\nClick 'Start' to launch server");
            }
        });

        // Start Server button - shown when disconnected
        Button startServerBtn = new Button("Start");
        String startBtnStyle = "-fx-background-color: #3b82f6; -fx-text-fill: white; -fx-border-radius: 6; -fx-background-radius: 6; -fx-padding: 4 12; -fx-cursor: hand; -fx-font-size: 11px; -fx-font-weight: 600;";
        String startBtnHover = "-fx-background-color: #2563eb; -fx-text-fill: white; -fx-border-radius: 6; -fx-background-radius: 6; -fx-padding: 4 12; -fx-cursor: hand; -fx-font-size: 11px; -fx-font-weight: 600;";
        startServerBtn.setStyle(startBtnStyle);
        startServerBtn.setOnMouseEntered(e -> startServerBtn.setStyle(startBtnHover));
        startServerBtn.setOnMouseExited(e -> startServerBtn.setStyle(startBtnStyle));
        Tooltip.install(startServerBtn, new Tooltip("Start AI Service (uvicorn server)"));
        startServerBtn.setOnAction(e -> {
            viewModel.logActivity("Starting AI Service...", MainViewModel.LogLevel.INFO);
            new Thread(() -> {
                try {
                    String projectPath = "/Users/joern/Documents/News/Absci corp/stock-news-pro";
                    ProcessBuilder pb = new ProcessBuilder(
                            "/bin/zsh", "-c",
                            "cd '" + projectPath
                                    + "' && source venv/bin/activate && uvicorn ai_service.main:app --port 8000 --reload");
                    pb.inheritIO();
                    pb.start();
                    // Wait a bit then check connection
                    Thread.sleep(3000);
                    Platform.runLater(() -> viewModel.checkConnection());
                } catch (Exception ex) {
                    Platform.runLater(() -> {
                        viewModel.logActivity("Failed to start server: " + ex.getMessage(),
                                MainViewModel.LogLevel.ERROR);
                    });
                }
            }).start();
        });
        // Hide button when connected
        viewModel.connectedProperty().addListener((obs, old, connected) -> {
            startServerBtn.setVisible(!connected);
            startServerBtn.setManaged(!connected);
        });

        bar.getChildren().addAll(tickerBox, sectorBox, langBox, spacer, spinner, analyzeBtn, exitBtn, startServerBtn,
                connectionDot);
        return bar;
    }

    private HBox createDashboard() {
        HBox dashboard = new HBox(20);
        dashboard.setPadding(new Insets(20, 24, 20, 24));
        dashboard.setAlignment(Pos.TOP_CENTER);

        // Left card: Market Overview
        VBox marketCard = createMarketOverviewCard();
        HBox.setHgrow(marketCard, Priority.ALWAYS);

        // Right card: Event Monitor
        VBox eventCard = createEventMonitorCard();
        HBox.setHgrow(eventCard, Priority.ALWAYS);

        dashboard.getChildren().addAll(marketCard, eventCard);
        return dashboard;
    }

    private VBox createMarketOverviewCard() {
        VBox card = new VBox(12);
        card.getStyleClass().add("card");
        card.setPrefWidth(580);

        // Header
        HBox header = new HBox(12);
        header.setAlignment(Pos.CENTER_LEFT);
        Label title = new Label("📈  Market Overview");
        title.getStyleClass().add("header");
        Region spacer = new Region();
        HBox.setHgrow(spacer, Priority.ALWAYS);
        header.getChildren().addAll(title, spacer);

        // ==================== 1. Executive Summary (TOP) ====================
        VBox summarySection = new VBox(6);
        summarySection.setPadding(new Insets(14));
        summarySection.setStyle(
                "-fx-background-color: #f0f9ff; -fx-background-radius: 10; -fx-border-color: #3b82f6; -fx-border-width: 0 0 0 4; -fx-border-radius: 0;");

        Label summaryTitle = new Label("📌 Executive Summary");
        summaryTitle.setStyle("-fx-font-size: 14px; -fx-font-weight: 700; -fx-text-fill: #1e40af;");

        Label summaryText = new Label(
                "Novo Nordisk profitiert stark vom Boom der Abnehmpräparate. Wegovy und Ozempic treiben das Wachstum.");
        summaryText.setWrapText(true);
        summaryText.setStyle("-fx-font-size: 12px; -fx-text-fill: #334155; -fx-line-spacing: 2;");
        summaryText.textProperty().bind(viewModel.analysisResultProperty());

        summarySection.getChildren().addAll(summaryTitle, summaryText);

        // ==================== 2. Quality & Valuation Metrics Card ====================
        VBox metricsCard = new VBox(12);
        metricsCard.setPadding(new Insets(16));
        metricsCard.setStyle(
                "-fx-background-color: white; -fx-background-radius: 12; -fx-border-color: #e2e8f0; -fx-border-radius: 12;");

        Label metricsTitle = new Label("💎 Quality & Valuation Metrics (Buffett/Lynch Style)");
        metricsTitle.setStyle("-fx-font-size: 14px; -fx-font-weight: 700; -fx-text-fill: #1e40af;");

        // Row 1: P/E, PEG, ROE (3 boxes)
        HBox metricsRow1 = new HBox(12);
        metricsRow1.setAlignment(Pos.CENTER);
        VBox peBox = createReportMetricBox("VALUATION: P/E RATIO", "42.50", "#1d1d1f");
        VBox pegBox = createReportMetricBox("GROWTH: PEG RATIO", "1.80", "#1d1d1f");
        VBox roeBox = createReportMetricBox("QUALITY: ROE", "88.5%", "#1d1d1f");
        metricsRow1.getChildren().addAll(peBox, pegBox, roeBox);

        // Row 2: Debt/Equity (1 box, left aligned)
        HBox metricsRow2 = new HBox(12);
        metricsRow2.setAlignment(Pos.CENTER_LEFT);
        VBox debtBox = createReportMetricBox("HEALTH: DEBT/EQUITY", "0.450", "#1d1d1f");
        metricsRow2.getChildren().add(debtBox);

        // ---- Analyst Targets Section (inside bordered card) ----
        VBox analystCard = new VBox(10);
        analystCard.setPadding(new Insets(12));
        analystCard.setStyle(
                "-fx-background-color: #fafafa; -fx-border-color: #e2e8f0; -fx-border-radius: 8; -fx-background-radius: 8;");

        HBox analystRow = new HBox(16);
        analystRow.setAlignment(Pos.CENTER);
        VBox targetMean = createReportMetricBox("ANALYST TARGET (MEAN)", "$145.00", "#1d1d1f");
        VBox targetHigh = createReportMetricBox("ANALYST HIGH", "$170.00", "#22c55e");
        VBox targetLow = createReportMetricBox("ANALYST LOW", "$120.00", "#ef4444");
        analystRow.getChildren().addAll(targetMean, targetHigh, targetLow);

        // Recommendation
        HBox recRow = new HBox(8);
        recRow.setAlignment(Pos.CENTER_LEFT);
        recRow.setPadding(new Insets(8, 0, 0, 0));
        Label recLabel = new Label("RECOMMENDATION");
        recLabel.setStyle("-fx-text-fill: #64748b; -fx-font-size: 10px; -fx-font-weight: 600;");
        Label recValue = new Label("BUY");
        recValue.setStyle("-fx-font-size: 14px; -fx-font-weight: 700; -fx-text-fill: #1d1d1f;");
        recRow.getChildren().addAll(recLabel, new Label("  "), recValue);

        analystCard.getChildren().addAll(analystRow, recRow);

        metricsCard.getChildren().addAll(metricsTitle, metricsRow1, metricsRow2, analystCard);

        // ==================== 3. Business Context (BOTTOM) ====================
        VBox contextSection = new VBox(4);
        contextSection.setPadding(new Insets(12, 0, 0, 0));

        Label contextLabel = new Label("Business Context: ");
        contextLabel.setStyle("-fx-font-size: 11px; -fx-font-weight: 700; -fx-text-fill: #1d1d1f;");

        Label contextText = new Label(
                "Novo Nordisk A/S, a healthcare company, engages in the research, development, manufacture, and marketing of pharmaceutical products worldwide. It operates in two segments, Diabetes and Obesity care and Rare Disease. The company offers products for treating diabetes and obesity including Ozempic, Wegovy, and Rybelsus.");
        contextText.setWrapText(true);
        contextText.setStyle("-fx-font-size: 11px; -fx-text-fill: #52525b; -fx-line-spacing: 1;");

        // Combine label and text in a flow
        javafx.scene.text.TextFlow contextFlow = new javafx.scene.text.TextFlow();
        javafx.scene.text.Text boldPart = new javafx.scene.text.Text("Business Context: ");
        boldPart.setStyle("-fx-font-size: 11px; -fx-font-weight: bold;");
        javafx.scene.text.Text normalPart = new javafx.scene.text.Text(
                "Novo Nordisk A/S, a healthcare company, engages in the research, development, manufacture, and marketing of pharmaceutical products worldwide. It operates in two segments, Diabetes and Obesity care and Rare Disease. The company offers products for treating diabetes and obesity including Ozempic, Wegovy, and Rybelsus.");
        normalPart.setStyle("-fx-font-size: 11px;");
        contextFlow.getChildren().addAll(boldPart, normalPart);

        contextSection.getChildren().add(contextFlow);

        // Use ScrollPane
        ScrollPane scrollPane = new ScrollPane();
        VBox content = new VBox(14);
        content.setPadding(new Insets(0, 4, 0, 0));
        content.getChildren().addAll(summarySection, metricsCard, contextSection);
        scrollPane.setContent(content);
        scrollPane.setFitToWidth(true);
        scrollPane.setStyle("-fx-background: transparent; -fx-background-color: transparent;");
        VBox.setVgrow(scrollPane, Priority.ALWAYS);

        card.getChildren().addAll(header, scrollPane);
        return card;
    }

    private VBox createReportMetricBox(String label, String value, String color) {
        VBox box = new VBox(4);
        box.setAlignment(Pos.CENTER);
        box.setPadding(new Insets(12, 18, 12, 18));
        box.setStyle(
                "-fx-background-color: #f8fafc; -fx-background-radius: 8; -fx-border-color: #e2e8f0; -fx-border-radius: 8;");

        Label lbl = new Label(label);
        lbl.setStyle("-fx-text-fill: #64748b; -fx-font-size: 9px; -fx-font-weight: 600;");

        Label val = new Label(value);
        val.setStyle("-fx-font-size: 18px; -fx-font-weight: 700; -fx-text-fill: " + color + ";");

        box.getChildren().addAll(lbl, val);
        return box;
    }

    private VBox createOutlookBox(String label, String value, String color) {
        VBox box = new VBox(2);
        box.setAlignment(Pos.CENTER);
        box.setPadding(new Insets(8, 16, 8, 16));
        box.setStyle("-fx-background-color: #f8f8f8; -fx-background-radius: 8;");

        Label lbl = new Label(label);
        lbl.setStyle("-fx-text-fill: #64748b; -fx-font-size: 10px;");

        Label val = new Label(value);
        val.setStyle("-fx-font-size: 12px; -fx-font-weight: 700; -fx-text-fill: " + color + ";");

        box.getChildren().addAll(lbl, val);
        return box;
    }

    private VBox createCompactMetricBox(String label, String value) {
        VBox box = new VBox(1);
        box.setAlignment(Pos.CENTER);
        box.setPadding(new Insets(8, 20, 8, 20));
        box.setStyle(
                "-fx-background-color: white; -fx-background-radius: 6; -fx-border-color: #e2e8f0; -fx-border-radius: 6;");

        Label lbl = new Label(label);
        lbl.setStyle("-fx-text-fill: #64748b; -fx-font-size: 9px; -fx-font-weight: 600;");

        Label val = new Label(value);
        val.setStyle("-fx-font-size: 14px; -fx-font-weight: 700; -fx-text-fill: #1d1d1f;");

        box.getChildren().addAll(lbl, val);
        return box;
    }

    private VBox createMetricBox(String label, String value, String color) {
        VBox box = new VBox(2);
        box.setAlignment(Pos.CENTER);
        box.setPadding(new Insets(10, 14, 10, 14));
        box.setStyle(
                "-fx-background-color: white; -fx-background-radius: 8; -fx-border-color: #e2e8f0; -fx-border-radius: 8;");

        Label lbl = new Label(label);
        lbl.setStyle("-fx-text-fill: #64748b; -fx-font-size: 9px; -fx-font-weight: 600;");

        Label val = new Label(value);
        val.setStyle("-fx-font-size: 18px; -fx-font-weight: 700; -fx-text-fill: " + color + ";");

        box.getChildren().addAll(lbl, val);
        return box;
    }

    private VBox createEventMonitorCard() {
        VBox card = new VBox(12);
        card.getStyleClass().add("card");
        card.setPrefWidth(450);

        // ==================== Large Chart Section ====================
        VBox chartSection = new VBox(8);
        chartSection.setPadding(new Insets(12));
        chartSection.setStyle("-fx-background-color: #f8fafc; -fx-background-radius: 10;");
        VBox.setVgrow(chartSection, Priority.ALWAYS);

        Label chartTitle = new Label("📈 Price Chart");
        chartTitle.setStyle("-fx-font-size: 13px; -fx-font-weight: 700; -fx-text-fill: #1e40af;");

        // Chart placeholder - LARGER
        VBox chartPlaceholder = new VBox();
        chartPlaceholder.setAlignment(Pos.CENTER);
        chartPlaceholder.setMinHeight(250);
        chartPlaceholder.setPrefHeight(300);
        chartPlaceholder.setStyle(
                "-fx-background-color: linear-gradient(to bottom, #e0f2fe, #f0f9ff); -fx-background-radius: 8;");
        VBox.setVgrow(chartPlaceholder, Priority.ALWAYS);

        Label chartLabel = new Label("📊 Chart will load after analysis");
        chartLabel.setStyle("-fx-text-fill: #64748b; -fx-font-size: 12px;");
        chartPlaceholder.getChildren().add(chartLabel);

        chartSection.getChildren().addAll(chartTitle, chartPlaceholder);

        // ==================== Single Top News ====================
        VBox newsSection = new VBox(6);
        newsSection.setPadding(new Insets(10));
        newsSection.setStyle(
                "-fx-background-color: #fefce8; -fx-background-radius: 8; -fx-border-color: #eab308; -fx-border-width: 0 0 0 3; -fx-border-radius: 0;");

        Label newsTitle = new Label("🔥 Top Story");
        newsTitle.setStyle("-fx-font-size: 12px; -fx-font-weight: 700; -fx-text-fill: #854d0e;");

        // Single news headline (first item from list, or placeholder)
        Label headline = new Label("No news yet - generate a report to see top story");
        headline.setWrapText(true);
        headline.setStyle("-fx-font-size: 11px; -fx-font-weight: 600; -fx-text-fill: #1d1d1f;");

        Label newsDate = new Label("");
        newsDate.setStyle("-fx-text-fill: #94a3b8; -fx-font-size: 10px;");

        // Bind to first news item
        viewModel.getNewsItems().addListener((javafx.collections.ListChangeListener<MainViewModel.NewsItem>) c -> {
            if (!viewModel.getNewsItems().isEmpty()) {
                MainViewModel.NewsItem first = viewModel.getNewsItems().get(0);
                headline.setText(first.getTitle());
                newsDate.setText(first.getSource() + " • " + first.getDate());
            } else {
                headline.setText("No news yet - generate a report to see top story");
                newsDate.setText("");
            }
        });

        newsSection.getChildren().addAll(newsTitle, headline, newsDate);

        card.getChildren().addAll(chartSection, newsSection);
        return card;
    }

    private VBox createStatBox(String value, String label, String color) {
        VBox box = new VBox(2);
        box.setAlignment(Pos.CENTER);
        box.setPadding(new Insets(12, 16, 12, 16));
        box.setStyle("-fx-background-color: #f5f5f7; -fx-background-radius: 10;");

        if (!label.isEmpty()) {
            Label lbl = new Label(label);
            lbl.setStyle("-fx-text-fill: #86868b; -fx-font-size: 10px;");
            box.getChildren().add(lbl);
        }
        Label val = new Label(value);
        val.setStyle("-fx-font-size: 16px; -fx-font-weight: 700; -fx-text-fill: " + color + ";");
        box.getChildren().add(val);
        return box;
    }

    private VBox createIndicatorBox(String label, String value, String color) {
        VBox box = new VBox(4);
        box.setAlignment(Pos.CENTER);
        box.setPadding(new Insets(12, 20, 12, 20));
        box.setStyle("-fx-background-color: #f8f8f8; -fx-background-radius: 10;");

        Label lbl = new Label(label);
        lbl.setStyle("-fx-text-fill: #86868b; -fx-font-size: 11px;");

        Label val = new Label(value);
        val.setStyle("-fx-font-size: 14px; -fx-font-weight: 700; -fx-text-fill: " + color + ";");

        box.getChildren().addAll(lbl, val);
        return box;
    }

    private HBox createStatusBar() {
        HBox bar = new HBox(10);
        bar.setAlignment(Pos.CENTER_LEFT);
        bar.setPadding(new Insets(10, 16, 10, 16));
        bar.getStyleClass().add("status-bar");

        Label status = new Label();
        status.textProperty().bind(viewModel.statusMessageProperty());

        Region spacer = new Region();
        HBox.setHgrow(spacer, Priority.ALWAYS);

        Label version = new Label("Stock News Pro v1.0 | © 2026 DeltaValue");
        version.setStyle("-fx-text-fill: #86868b; -fx-font-size: 11px;");

        bar.getChildren().addAll(status, spacer, version);
        return bar;
    }

    public static void main(String[] args) {
        launch();
    }

    private void setupAutocomplete(ComboBox<String> comboBox, StringProperty property) {
        ObservableList<String> items = FXCollections.observableArrayList(comboBox.getItems());

        // 1. Select All on Focus
        comboBox.getEditor().setOnMouseClicked(e -> comboBox.getEditor().selectAll());
        comboBox.getEditor().focusedProperty().addListener((obs, wasFocused, isNowFocused) -> {
            if (isNowFocused) {
                Platform.runLater(comboBox.getEditor()::selectAll);
            }
        });

        // 2. Autocomplete Logic
        comboBox.getEditor().textProperty().addListener((obs, oldText, newText) -> {
            // Update ViewModel immediately
            property.set(newText);

            // Filter items
            if (newText == null || newText.isEmpty()) {
                comboBox.setItems(items);
                return;
            }

            // Don't filter if it's an exact match (selected)
            boolean exactMatch = items.stream().anyMatch(item -> item.equalsIgnoreCase(newText));
            if (exactMatch && !comboBox.isShowing())
                return;

            ObservableList<String> filtered = FXCollections.observableArrayList();
            for (String item : items) {
                if (item.toLowerCase().contains(newText.toLowerCase())) {
                    filtered.add(item);
                }
            }
            comboBox.setItems(filtered);

            // Show popup if results found and we are typing (focused)
            if (!filtered.isEmpty() && comboBox.getEditor().isFocused()) {
                if (!comboBox.isShowing())
                    comboBox.show();
            } else {
                comboBox.hide();
            }
        });

        // 3. Sync from ViewModel back to Edge
        property.addListener((obs, o, n) -> {
            if (n != null && !n.equals(comboBox.getEditor().getText())) {
                comboBox.getEditor().setText(n);
            }
        });
    }
}
