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
import javafx.scene.control.ToggleButton;
import javafx.scene.control.ToggleGroup;
import javafx.scene.control.Tooltip;
import javafx.scene.chart.CategoryAxis;
import javafx.scene.chart.LineChart;
import javafx.scene.chart.NumberAxis;
import javafx.scene.chart.XYChart;

/**
 * Stock News Pro - Modern Dashboard UI
 * 
 * Clean, professional interface matching the DeltaValue design language.
 * Features: Ticker input, Sector dropdown, Language selection, Report
 * generation.
 */
public class MainApp extends Application {

    private MainViewModel viewModel;

    // ==================== UI CONSTANTS (The "Critical Lens" Palette)
    // ====================
    private static final String COLOR_BG_CARD = "#f1f5f9"; // Slate-100
    private static final String COLOR_BG_WHITE = "#ffffff";
    private static final String COLOR_TEXT_PRIMARY = "#1e293b"; // Slate-800
    private static final String COLOR_TEXT_SECONDARY = "#64748b"; // Slate-500
    private static final String COLOR_ACCENT = "#2563eb"; // Blue-800 (Updated from #1e40af)
    private static final String COLOR_BORDER_LIGHT = "#e2e8f0";
    private static final String COLOR_TEXT_MUTED = "#94a3b8"; // Restored missing constant

    // Typography - dynamic sizing applied via bindResponsiveFont
    private static final String STYLE_CARD_BASE = "-fx-background-radius: 12; -fx-effect: dropshadow(three-pass-box, rgba(0,0,0,0.03), 4, 0, 0, 2);";

    private enum BoxStyle {
        CARD, FRAMELESS
    }

    // Global Scale Property (derived from window width)
    private javafx.beans.property.DoubleProperty uiScale = new javafx.beans.property.SimpleDoubleProperty(1.0);

    @Override
    public void start(Stage stage) {
        viewModel = new MainViewModel();

        // Initialize scale
        uiScale.set(1.0);

        // Bind Scale Property: Base width 1200px
        // logic: SQRT scaling curve (User: "Editorial Layout")
        // formula: sqrt(width/1200) clamped [0.9, 1.35]
        stage.widthProperty().addListener((obs, oldW, newW) -> {
            double width = newW.doubleValue();
            if (Double.isNaN(width) || width == 0)
                width = 1200;

            // Reverted to 1350 per user request ("Make font bigger again")
            // This restores the original scale while we fix the metric box layout via CSS
            double scale = width / 1350.0;

            // Loose clamping to prevent extreme edge cases
            scale = Math.max(0.5, Math.min(2.5, scale));
            uiScale.set(scale);
        });

        // Main layout
        BorderPane root = new BorderPane();
        root.getStyleClass().add("root");

        // Root Font Scaling: "The One Ring to Rule Them All"
        // This allows natural scaling of all non-explicitly-bound elements (Buttons,
        // Labels, etc.)
        root.styleProperty().bind(javafx.beans.binding.Bindings.createStringBinding(
                () -> String.format(java.util.Locale.US, "-fx-font-size: %.1fpx;", 13 * uiScale.get()), // reduced base
                                                                                                        // from 14 to 13
                uiScale));

        // Top: Clean input bar
        HBox topBar = createTopBar();
        root.setTop(topBar);

        // Center: Dashboard cards
        HBox dashboard = createDashboard();
        root.setCenter(dashboard);

        // Bottom: Minimal status bar
        HBox statusBar = createStatusBar();
        root.setBottom(statusBar);

        // Initial preferred size - Standard Desktop Size, no 80% limit
        double prefWidth = 1200;
        double prefHeight = 850;

        Scene scene = new Scene(root, prefWidth, prefHeight);
        scene.getStylesheets().add(getClass().getResource("/styles/main.css") != null
                ? getClass().getResource("/styles/main.css").toExternalForm()
                : "");

        stage.setScene(scene);
        stage.setTitle("Stock News Pro");

        // Initial Size & Focus
        stage.setWidth(1280);
        stage.setHeight(800);
        stage.centerOnScreen();
        stage.show();

        // Focus Fix: Ensure window is active on startup (Fixes "Icon wackeln/Inaktiv")
        stage.toFront();
        stage.requestFocus();

        // Set min/max constraints
        stage.setMinWidth(800);
        stage.setMinHeight(600);
        stage.setMaxWidth(Double.MAX_VALUE);
        stage.setMaxHeight(Double.MAX_VALUE);

        stage.setOnCloseRequest(e -> {
            Platform.exit();
            System.exit(0);
        });
        // Auto-connect on startup
        viewModel.checkConnection();
        // Load initial data for chart
        viewModel.loadPriceHistory();
    }

    @Override
    public void stop() {
        System.out.println("App stopping... killing background threads.");

        // 1. Kill Python Backend (Nuclear Option)
        new Thread(() -> {
            try {
                // pkill -f matches full command line
                new ProcessBuilder("/bin/zsh", "-c", "pkill -f 'uvicorn ai_service.main:app'").start();
                System.out.println("Sent kill signal to API server.");
            } catch (Exception ex) {
                System.err.println("Failed to kill server: " + ex.getMessage());
            }
        }).start();

        // 2. Stop Timelines in ViewModel
        // (Assuming we might add a shutdown method to ViewModel later, but for now
        // system exit does it)

        // 3. Force Kill JVM to stop HttpClient threads
        // Using a short delay to allow pkill to fire? No, pkill is async process.
        // We just exit.
        System.out.println("Exiting JVM.");
        System.exit(0);
    }

    // Removed manual scaling helpers (bindScaledPadding, bindScaledSpacing) to
    // relies on CSS and Layout Engine

    private HBox createTopBar() {
        HBox bar = new HBox(20); // Static spacing instead of bindScaledSpacing
        bar.setPadding(new Insets(16, 24, 16, 24)); // Static padding instead of bindScaledPadding
        bar.setAlignment(Pos.CENTER_LEFT);
        bar.setStyle("-fx-background-color: white; -fx-border-color: #e5e5ea; -fx-border-width: 0 0 1 0;");

        double inputWidth = 180;
        double inputHeight = 36;
        String inputStyle = "-fx-background-color: white; -fx-border-color: #d2d2d7; -fx-border-radius: 6; -fx-background-radius: 6;";

        // Ticker input with label
        VBox tickerBox = new VBox(4);
        tickerBox.setAlignment(Pos.CENTER_LEFT);
        Label tickerLabel = new Label("Aktie");
        tickerLabel.setStyle("-fx-text-fill: #86868b;");
        tickerLabel.setStyle("-fx-font-weight: 800; -fx-text-fill: " + COLOR_TEXT_MUTED + "; -fx-font-size: 0.65em;");

        TextField tickerField = new TextField();
        tickerField.setPromptText("z.B. NVO, GOOG, TSLA...");
        tickerField.setPrefWidth(inputWidth); // Could bind this too if needed
        tickerField.setPrefHeight(inputHeight);
        tickerField.setStyle(inputStyle);
        tickerField.fontProperty().bind(javafx.beans.binding.Bindings.createObjectBinding(
                () -> javafx.scene.text.Font.font("System", 13 * uiScale.get()), uiScale));
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
        analyzeBtn.getStyleClass().add("primary");
        analyzeBtn.setStyle("-fx-font-size: 0.95em;");

        analyzeBtn.setOnAction(e -> viewModel.exportHtmlReport());
        analyzeBtn.disableProperty().bind(viewModel.loadingProperty().or(viewModel.connectedProperty().not()));

        // Exit button - subtle red outline style
        Button exitBtn = new Button("Exit");
        exitBtn.getStyleClass().add("secondary"); // Assuming a secondary style for exit
        exitBtn.setStyle("-fx-font-size: 0.95em;");

        exitBtn.setOnAction(e -> {
            // Trigger standard JavaFX shutdown sequence
            Platform.exit();
        });

        // Connection dot with Tooltip
        Label connectionDot = new Label("●");
        connectionDot.setStyle("-fx-text-fill: #ef4444;"); // Color only, font handled by bindResponsiveFont
        connectionDot.setStyle("-fx-text-fill: #ef4444; -fx-font-size: 1.3em;");

        Tooltip connectionTooltip = new Tooltip("❌ Disconnected: Checking...");
        connectionTooltip.setStyle("-fx-font-size: 12px;");
        connectionTooltip.setShowDelay(javafx.util.Duration.ZERO);
        connectionTooltip.setHideDelay(javafx.util.Duration.seconds(3));
        Tooltip.install(connectionDot, connectionTooltip);
        viewModel.connectedProperty().addListener((obs, old, connected) -> {
            if (connected) {
                connectionDot.setStyle("-fx-text-fill: #22c55e;");
                connectionTooltip.setText("✅ Connected: AI Service running at localhost:8000");
            } else {
                connectionDot.setStyle("-fx-text-fill: #ef4444;");
                connectionTooltip.setText(
                        "❌ Disconnected: Cannot reach localhost:8000\nClick 'Start' to launch server");
            }
        });

        // Start Server button - shown when disconnected
        Button startServerBtn = new Button("Start");
        startServerBtn.getStyleClass().add("start-server-button"); // Assuming a specific style class
        startServerBtn.setStyle("-fx-font-size: 0.9em;");

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
        HBox dashboard = new HBox(20); // Static spacing
        dashboard.setPadding(new Insets(20, 24, 20, 24)); // Static padding
        dashboard.setAlignment(Pos.TOP_CENTER);

        // Left card: Market Overview
        VBox marketCard = createMarketOverviewCard();
        HBox.setHgrow(marketCard, Priority.ALWAYS);
        marketCard.setPrefWidth(0); // Force equal distribution (Zero-Basis)

        // Right card: Event Monitor
        VBox eventCard = createEventMonitorCard();
        HBox.setHgrow(eventCard, Priority.ALWAYS);
        eventCard.setPrefWidth(0); // Force equal distribution (Zero-Basis)

        dashboard.getChildren().addAll(marketCard, eventCard);
        return dashboard;
    }

    private VBox createMarketOverviewCard() {
        VBox card = new VBox(12); // Static spacing
        card.getStyleClass().add("card");
        card.setPadding(new Insets(16)); // Static padding
        card.setMinWidth(100);

        // Header
        HBox header = new HBox(12);
        header.setAlignment(Pos.CENTER_LEFT);
        Label title = new Label("📈  Market Overview");
        title.getStyleClass().add("header");
        // Font size handled by CSS inheritance or specific class, minimal manual
        // binding if needed
        title.setStyle("-fx-font-size: 1.25em;");

        Region spacer = new Region();
        HBox.setHgrow(spacer, Priority.ALWAYS);
        header.getChildren().addAll(title, spacer);

        // ==================== 1. Executive Summary (TOP) ====================
        VBox summarySection = new VBox(6);
        summarySection.setPadding(new Insets(14));
        summarySection.setStyle(
                "-fx-background-color: #f0f9ff; -fx-background-radius: 10; -fx-border-color: #3b82f6; -fx-border-width: 0 0 0 4; -fx-border-radius: 0;");

        Label summaryTitle = new Label("📌 Executive Summary");
        summaryTitle.setStyle("-fx-font-weight: 700; -fx-text-fill: #1e40af;");
        summaryTitle.setStyle("-fx-font-weight: 700; -fx-text-fill: #1e40af; -fx-font-size: 1.0em;");

        Label summaryText = new Label();
        summaryText.setWrapText(true);
        // Blocksatz REMOVED per User Instruction ("Nie justify")
        // Use LEFT alignment for stability
        summaryText.setTextAlignment(javafx.scene.text.TextAlignment.LEFT);
        summaryText.setStyle("-fx-text-fill: #334155; -fx-line-spacing: 2;");
        summaryText.setStyle("-fx-text-fill: #334155; -fx-line-spacing: 2; -fx-font-size: 0.95em;");

        summaryText.textProperty().bind(viewModel.executiveSummaryProperty());

        summarySection.getChildren().addAll(summaryTitle, summaryText);

        // ==================== METRICS CONTAINER ====================
        VBox metricsContainer = new VBox(16);
        metricsContainer.setPadding(new Insets(20));
        metricsContainer.setStyle("-fx-background-color: " + COLOR_BG_CARD + "; -fx-border-color: " + COLOR_BORDER_LIGHT
                + "; " + STYLE_CARD_BASE);

        Label metricsTitle = new Label("💎 Quality & Valuation Metrics (Buffett/Lynch Style)");
        metricsTitle.setStyle("-fx-font-weight: 700; -fx-text-fill: " + COLOR_ACCENT + ";");
        metricsTitle.setStyle("-fx-font-weight: 700; -fx-text-fill: " + COLOR_ACCENT + "; -fx-font-size: 1.1em;");

        // --- ROW 1: Fundamentals (4 Items) ---
        // Natural Row: 4 items, spaced naturally (15px gap)
        HBox row1 = createMetricRow(
                createMetricBox("VALUATION: P/E", viewModel.peRatioProperty(), "#1d1d1f", BoxStyle.CARD),
                createMetricBox("GROWTH: PEG", viewModel.pegRatioProperty(), "#1d1d1f", BoxStyle.CARD),
                createMetricBox("QUALITY: ROE", viewModel.roeProperty(), "#1d1d1f", BoxStyle.CARD),
                createMetricBox("HEALTH: D/E", viewModel.debtToEquityProperty(), "#1d1d1f", BoxStyle.CARD));

        // --- ROW 2: Analyst Targets (3 Items) ---
        // Natural Row: 3 items
        HBox row2 = createMetricRow(
                createMetricBox("TARGET (MEAN)", viewModel.targetMeanProperty(), "#1d1d1f", BoxStyle.CARD),
                createMetricBox("TARGET HIGH", viewModel.targetHighProperty(), "#22c55e", BoxStyle.CARD),
                createMetricBox("TARGET LOW", viewModel.targetLowProperty(), "#ef4444", BoxStyle.CARD));

        // --- ROW 3: Recommendation (1 Item) ---
        // Natural Row: 1 item.
        // Sizing managed by CSS padding (increased in main.css).
        HBox row3 = createMetricRow(
                createMetricBox("RECOMMENDATION", viewModel.recommendationProperty(), "#1d1d1f", BoxStyle.CARD));

        // --- Separator & Business Context Group (Tighter Spacing) ---
        VBox bottomGroup = new VBox(6);

        // Separator
        javafx.scene.shape.Line separator = new javafx.scene.shape.Line(0, 0, 100, 0);
        separator.setStroke(javafx.scene.paint.Color.web(COLOR_BORDER_LIGHT));
        separator.getStrokeDashArray().addAll(4d, 4d);
        separator.endXProperty().bind(metricsContainer.widthProperty().subtract(40));

        HBox sepBox = new HBox(separator);
        sepBox.setAlignment(Pos.CENTER);
        sepBox.setPadding(new Insets(4, 0, 0, 0));
        HBox.setHgrow(separator, Priority.ALWAYS); // Separator fills width

        // Business Context Text
        javafx.scene.text.TextFlow contextFlow = new javafx.scene.text.TextFlow();
        // Blocksatz REMOVED per User Instruction ("Nie justify")
        contextFlow.setTextAlignment(javafx.scene.text.TextAlignment.LEFT);

        javafx.scene.text.Text boldPart = new javafx.scene.text.Text("Business Context: ");
        boldPart.setStyle("-fx-font-weight: 800; -fx-fill: " + COLOR_TEXT_PRIMARY + ";");
        // Simplified font binding or use styles
        boldPart.setFont(javafx.scene.text.Font.font("System", javafx.scene.text.FontWeight.BOLD, 12));

        javafx.scene.text.Text businessText = new javafx.scene.text.Text();
        businessText.textProperty().bind(viewModel.businessSummaryProperty());
        // Text nodes in TextFlow wrap automatically based on container width
        businessText.setStyle("-fx-fill: " + COLOR_TEXT_SECONDARY + "; -fx-font-size: 0.9em;");

        contextFlow.getChildren().add(boldPart);
        contextFlow.getChildren().add(businessText);
        // Removed manual width binding: contextFlow.prefWidthProperty().bind(...)
        contextFlow.setMaxWidth(Double.MAX_VALUE);

        bottomGroup.getChildren().addAll(sepBox, contextFlow);
        metricsContainer.getChildren().addAll(metricsTitle, row1, row2, row3, bottomGroup);

        card.getChildren().add(metricsContainer);

        // Use CenteredContentPane (Editorial Layout)
        // Max Width: 820px
        com.news_ai.stock.ui.layout.CenteredContentPane centerPane = new com.news_ai.stock.ui.layout.CenteredContentPane(
                820, 14);

        // Add sections to the centered content
        centerPane.add(summarySection);
        centerPane.add(metricsContainer);

        // Wrapping in ScrollPane for scrollability
        ScrollPane scrollPane = new ScrollPane();
        scrollPane.setContent(centerPane);
        scrollPane.setFitToWidth(true);
        scrollPane.setStyle("-fx-background: transparent; -fx-background-color: transparent;");
        VBox.setVgrow(scrollPane, Priority.ALWAYS);

        card.getChildren().addAll(header, scrollPane);
        return card;
    }

    /**
     * Creates a metric row that fills the available width (Safe inside
     * CenteredContentPane).
     * - Uses HGrow.ALWAYS to fill the 820px editorial width.
     */
    private HBox createMetricRow(VBox... items) {
        HBox row = new HBox(15);
        row.setAlignment(Pos.CENTER_LEFT);
        for (VBox item : items) {
            item.setMaxWidth(Double.MAX_VALUE);
            HBox.setHgrow(item, Priority.ALWAYS);
            row.getChildren().add(item);
        }
        return row;
    }

    /**
     * Helper to bind font size to window size for responsive text.
     * Uses min(width, height) to prevent aggressive scaling on wide/tall screens.
     */
    /**
     * Helper to bind font size to window size for responsive text.
     * Uses min(width, height) to prevent aggressive scaling on wide/tall screens.
     */
    // bindResponsiveFont removed to rely on Root Font Scaling

    // Legacy helper not needed anymore
    // private void updateFont...

    /**
     * Unified Metric Box Creator - Eliminates "code slop" and duplication.
     */
    private VBox createMetricBox(String label, javafx.beans.property.StringProperty valueProperty, String valueColor,
            BoxStyle style) {
        VBox box = new VBox(4); // Static spacing - could be updated to use CSS spacing if VBox supported it
                                // easily,
                                // but spacing is property.
        box.setAlignment(Pos.CENTER);
        box.setMinWidth(40);
        box.getStyleClass().add("metric-box"); // CSS class for padding and background

        if (style == BoxStyle.CARD) {
            box.getStyleClass().add("metric-box-card");
        } else {
            box.getStyleClass().add("metric-box-transparent");
        }

        Label lbl = new Label(label);
        lbl.getStyleClass().add("metric-label");

        Label val = new Label();
        val.textProperty().bind(valueProperty);
        val.getStyleClass().add("metric-value");
        // We still need to apply color dynamically as it varies per metric
        // (green/red/black)
        val.setStyle("-fx-text-fill: " + valueColor + ";");

        box.getChildren().addAll(lbl, val);
        return box;
    }

    private VBox createEventMonitorCard() {
        VBox card = new VBox(12); // Static spacing
        card.getStyleClass().add("card");
        card.setPadding(new Insets(16)); // Static padding
        card.setMinWidth(100);

        // ==================== Chart Header & Controls ====================
        HBox chartHeader = new HBox(10);
        chartHeader.setAlignment(Pos.CENTER_LEFT);

        Label chartTitle = new Label("📈 Price Chart");
        chartTitle.setStyle("-fx-text-fill: " + COLOR_ACCENT + "; -fx-font-weight: 700; -fx-font-size: 1.2em;");

        chartTitle.setStyle("-fx-text-fill: " + COLOR_ACCENT + "; -fx-font-weight: 700;");

        Region headerSpacer = new Region();
        HBox.setHgrow(headerSpacer, Priority.ALWAYS);

        // Period Selector
        HBox periodSelector = new HBox(4);
        ToggleGroup periodGroup = new ToggleGroup();

        String[] periods = { "10y", "1y", "3m", "1m", "1w", "24h" };
        for (String p : periods) {
            ToggleButton btn = new ToggleButton(p.toUpperCase());
            btn.setStyle("-fx-font-size: 0.8em;"); // Relative scale

            btn.setToggleGroup(periodGroup);
            btn.setUserData(p);

            // Style
            btn.getStyleClass().add("period-button"); // Needs CSS
            btn.setStyle("-fx-background-color: transparent; -fx-text-fill: " + COLOR_TEXT_SECONDARY
                    + "; -fx-border-color: " + COLOR_BORDER_LIGHT + "; -fx-border-radius: 4;");

            btn.selectedProperty().addListener((obs, oldVal, newVal) -> {
                if (newVal) {
                    btn.setStyle("-fx-background-color: " + COLOR_ACCENT
                            + "; -fx-text-fill: #ffffff; -fx-background-radius: 4;");
                    viewModel.selectedChartPeriodProperty().set(p);
                    viewModel.loadPriceHistory();
                } else {
                    btn.setStyle("-fx-background-color: transparent; -fx-text-fill: " + COLOR_TEXT_SECONDARY
                            + "; -fx-border-color: " + COLOR_BORDER_LIGHT + "; -fx-border-radius: 4;");
                }
            });

            if (p.equals("1y"))
                btn.setSelected(true);
            periodSelector.getChildren().add(btn);
        }

        chartHeader.getChildren().addAll(chartTitle, headerSpacer, periodSelector);

        // ==================== Line Chart ====================
        VBox chartSection = new VBox(8); // Static spacing
        chartSection.setPadding(new Insets(12));
        chartSection.setStyle("-fx-background-color: #f8fafc; -fx-background-radius: 10;");
        VBox.setVgrow(chartSection, Priority.ALWAYS);

        // Axes
        CategoryAxis xAxis = new CategoryAxis();
        NumberAxis yAxis = new NumberAxis();
        xAxis.setAnimated(false);
        yAxis.setAnimated(false);
        yAxis.setForceZeroInRange(false); // Auto-scale Y axis

        LineChart<String, Number> lineChart = new LineChart<>(xAxis, yAxis);
        lineChart.setAnimated(false);
        lineChart.setLegendVisible(false);
        lineChart.setCreateSymbols(false); // No dots on line
        lineChart.setMinHeight(200);
        VBox.setVgrow(lineChart, Priority.ALWAYS);

        // Remove chart border/background to blend in
        lineChart.setStyle("-fx-background-color: transparent;");
        lineChart.lookup(".chart-plot-background").setStyle("-fx-background-color: transparent;");

        XYChart.Series<String, Number> series = new XYChart.Series<>();
        lineChart.getData().add(series);

        // Data Binding
        viewModel.getPriceHistory().addListener((javafx.collections.ListChangeListener<MainViewModel.PricePoint>) c -> {
            Platform.runLater(() -> {
                try {
                    System.out
                            .println("DEBUG: Chart Listener Triggered. Points: " + viewModel.getPriceHistory().size());
                    series.getData().clear();
                    for (MainViewModel.PricePoint pp : viewModel.getPriceHistory()) {
                        series.getData().add(new XYChart.Data<>(pp.getLabel(), pp.getClose()));
                    }

                    // Dynamic styling based on trend
                    if (viewModel.getPriceHistory().size() > 1) {
                        double start = viewModel.getPriceHistory().get(0).getClose();
                        double end = viewModel.getPriceHistory().get(viewModel.getPriceHistory().size() - 1).getClose();
                        String color = end >= start ? "#16a34a" : "#dc2626"; // Green or Red
                        series.getNode().setStyle("-fx-stroke: " + color + "; -fx-stroke-width: 2px;");
                    }
                } catch (Exception ex) {
                    System.err.println("CRITICAL: Failed to update chart: " + ex.getMessage());
                    ex.printStackTrace();
                }
            });
        });

        // Also reload chart when ticker changes
        viewModel.selectedTickerProperty().addListener((obs, old, newTicker) -> {
            viewModel.loadPriceHistory();
        });

        // Add 24h Date Label
        Label dateLabel = new Label();
        dateLabel.textProperty().bind(viewModel.chartDateLabelProperty());
        dateLabel.setStyle("-fx-text-fill: " + COLOR_TEXT_SECONDARY + "; -fx-font-style: italic;");
        dateLabel.setStyle("-fx-text-fill: #94a3b8;"); // Inherits size

        HBox chartFooter = new HBox(dateLabel);
        chartFooter.setAlignment(Pos.CENTER_RIGHT);

        chartSection.getChildren().addAll(chartHeader, lineChart, chartFooter);

        // ==================== Sector News Ticker ====================
        VBox newsSection = new VBox(6);
        newsSection.setPadding(new Insets(10));
        newsSection.setStyle(
                "-fx-background-color: #fefce8; -fx-background-radius: 8; -fx-border-color: #eab308; -fx-border-width: 0 0 0 3; -fx-border-radius: 0;");

        Label newsTitle = new Label("📣 Sector News");
        newsTitle.setStyle("-fx-font-weight: 700; -fx-text-fill: #854d0e;");
        newsTitle.setStyle("-fx-text-fill: #1e40af; -fx-padding: 0;"); // Inherits size

        // Ticker implementation using AnimationTimer would be best, but simple Label
        // for now
        Label tickerLabel = new Label("Loading sector news...");
        tickerLabel.setWrapText(true);
        tickerLabel.setStyle("-fx-font-weight: 600; -fx-text-fill: #1d1d1f;");
        tickerLabel.setStyle("-fx-text-fill: #334155; -fx-padding: 0 0 0 0; -fx-font-weight: bold;"); // Inherits size,
                                                                                                      // force bold

        // Bind to sector news
        viewModel.getSectorNews()
                .addListener((javafx.collections.ListChangeListener<MainViewModel.SectorNewsItem>) c -> {
                    if (!viewModel.getSectorNews().isEmpty()) {
                        StringBuilder sb = new StringBuilder();
                        for (MainViewModel.SectorNewsItem item : viewModel.getSectorNews()) {
                            if (sb.length() > 0)
                                sb.append("  •  ");
                            sb.append(item.toString());
                        }
                        tickerLabel.setText(sb.toString());
                    } else {
                        tickerLabel.setText("No news available for this sector.");
                    }
                });

        // Reload news when sector changes
        viewModel.selectedSectorProperty().addListener((obs, old, newSector) -> {
            viewModel.loadSectorNews();
        });

        newsSection.getChildren().addAll(newsTitle, tickerLabel);

        card.getChildren().addAll(chartSection, newsSection);
        return card;
    }

    // ... (createMetricBox modification needed separately) ...

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
