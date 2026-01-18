package com.news_ai.stock.viewmodel;

import com.news_ai.stock.service.ApiService;
import javafx.application.Platform;
import javafx.beans.property.*;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import javafx.animation.KeyFrame;
import javafx.animation.Timeline;
import javafx.util.Duration;
import java.util.List;

/**
 * ViewModel for the main application view.
 * Manages state and business logic following MVVM pattern.
 */
public class MainViewModel {

    // Use platform-specific formatting for the log
    private static final DateTimeFormatter TIME_FORMAT = DateTimeFormatter.ofPattern("HH:mm:ss.SSS");

    private final ApiService apiService;
    private Timeline rateLimitTimeline;

    // Observable Properties for UI binding
    private final BooleanProperty connected = new SimpleBooleanProperty(false);
    private final BooleanProperty loading = new SimpleBooleanProperty(false);
    private final BooleanProperty rateLimited = new SimpleBooleanProperty(false);
    private final StringProperty statusMessage = new SimpleStringProperty("Not connected");
    private final StringProperty analysisResult = new SimpleStringProperty("");
    private final StringProperty rateLimitMessage = new SimpleStringProperty("");
    private final StringProperty selectedTicker = new SimpleStringProperty("ABSI");
    private final StringProperty selectedSector = new SimpleStringProperty("Biotechnology");
    private final StringProperty selectedLanguage = new SimpleStringProperty("German");
    private final StringProperty reportPath = new SimpleStringProperty("");
    private final ObservableList<NewsItem> newsItems = FXCollections.observableArrayList();
    private final ObservableList<String> activityLog = FXCollections.observableArrayList();

    // Fundamentals Properties for dynamic UI binding
    private final StringProperty peRatio = new SimpleStringProperty("-");
    private final StringProperty pegRatio = new SimpleStringProperty("-");
    private final StringProperty roe = new SimpleStringProperty("-");
    private final StringProperty debtToEquity = new SimpleStringProperty("-");
    private final StringProperty targetMean = new SimpleStringProperty("-");
    private final StringProperty targetHigh = new SimpleStringProperty("-");
    private final StringProperty targetLow = new SimpleStringProperty("-");
    private final StringProperty recommendation = new SimpleStringProperty("-");
    private final StringProperty businessSummary = new SimpleStringProperty("");
    private final StringProperty executiveSummary = new SimpleStringProperty("");

    // Chart Properties
    private final StringProperty selectedChartPeriod = new SimpleStringProperty("1y");
    private final ObservableList<PricePoint> priceHistory = FXCollections.observableArrayList();
    private final StringProperty chartDateLabel = new SimpleStringProperty(""); // For 24h mode
    private final BooleanProperty chartIsHistorical = new SimpleBooleanProperty(false);

    // Sector News Properties
    private final ObservableList<SectorNewsItem> sectorNews = FXCollections.observableArrayList();

    public enum LogLevel {
        INFO, WARN, ERROR, DEBUG
    }

    public MainViewModel() {
        this(new ApiService());
    }

    public MainViewModel(ApiService apiService) {
        this.apiService = apiService;
        logActivity("Application started", LogLevel.INFO);
    }

    // ... (rest of the file)

    // Helper to log with default level
    public void logActivity(String message) {
        logActivity(message, LogLevel.INFO);
    }

    /**
     * Log an activity message with timestamp and level.
     */
    public void logActivity(String message, LogLevel level) {
        String timestamp = LocalDateTime.now().format(TIME_FORMAT);
        String logEntry = String.format("[%s] [%s] %s", timestamp, level, message);

        // Use Platform.runLater only if toolkit is initialized
        try {
            if (javafx.application.Platform.isFxApplicationThread()) {
                activityLog.add(logEntry);
                if (activityLog.size() > 1000) { // Increased log size
                    activityLog.remove(0);
                }
            } else {
                Platform.runLater(() -> {
                    activityLog.add(logEntry);
                    if (activityLog.size() > 1000) {
                        activityLog.remove(0);
                    }
                });
            }
        } catch (IllegalStateException e) {
            // Toolkit not initialized (in tests), add directly
            activityLog.add(logEntry);
            if (activityLog.size() > 1000) {
                activityLog.remove(0);
            }
        }
    }

    // ==================== Rate Limit ====================

    /**
     * Check rate limit status from AI Service.
     */
    public void checkRateLimitStatus() {
        apiService.getRateLimitStatus()
                .thenAccept(response -> Platform.runLater(() -> {
                    if (response.isSuccess()) {
                        String body = response.getBody();
                        // Parse rate_limited field
                        boolean isLimited = body.contains("\"rate_limited\":true");
                        setRateLimited(isLimited);

                        if (isLimited) {
                            // Extract remaining_seconds
                            int remaining = extractSeconds(body);
                            startRateLimitCountdown(remaining);
                            logActivity("Rate limited for " + remaining + " seconds", LogLevel.WARN);
                        } else {
                            stopRateLimitCountdown();
                            setRateLimitMessage("");
                        }
                    }
                }));
    }

    private void startRateLimitCountdown(int seconds) {
        if (rateLimitTimeline != null) {
            rateLimitTimeline.stop();
        }

        final int[] remaining = { seconds };
        setRateLimitMessage("Rate limit: " + remaining[0] + "s");

        rateLimitTimeline = new Timeline(new KeyFrame(Duration.seconds(1), e -> {
            remaining[0]--;
            if (remaining[0] > 0) {
                setRateLimitMessage("Rate limit: " + remaining[0] + "s");
            } else {
                setRateLimitMessage("");
                setRateLimited(false);
                rateLimitTimeline.stop();
            }
        }));
        rateLimitTimeline.setCycleCount(Timeline.INDEFINITE);
        rateLimitTimeline.play();
    }

    private void stopRateLimitCountdown() {
        if (rateLimitTimeline != null) {
            rateLimitTimeline.stop();
        }
    }

    private int extractSeconds(String json) {
        try {
            int start = json.indexOf("\"remaining_seconds\":") + 20;
            int end = json.indexOf(",", start);
            if (end == -1)
                end = json.indexOf("}", start);
            return Integer.parseInt(json.substring(start, end).trim());
        } catch (Exception e) {
            return 0;
        }
    }

    // Rate limit property getters/setters
    public boolean isRateLimited() {
        return rateLimited.get();
    }

    public BooleanProperty rateLimitedProperty() {
        return rateLimited;
    }

    public void setRateLimited(boolean value) {
        rateLimited.set(value);
    }

    public String getRateLimitMessage() {
        return rateLimitMessage.get();
    }

    public StringProperty rateLimitMessageProperty() {
        return rateLimitMessage;
    }

    public void setRateLimitMessage(String value) {
        rateLimitMessage.set(value);
    }

    // ==================== Commands ====================

    /**
     * Check connection to AI Service.
     */
    public void checkConnection() {
        setLoading(true);
        setStatusMessage("Checking connection...");
        logActivity("Checking connection to AI Service...");

        apiService.checkHealth()
                .thenAccept(healthy -> Platform.runLater(() -> {
                    setConnected(healthy);
                    setStatusMessage(healthy ? "Connected to AI Service" : "Connection failed");
                    if (healthy) {
                        logActivity("Connected successfully", LogLevel.INFO);
                    } else {
                        logActivity("Connection failed", LogLevel.ERROR);
                    }
                    setLoading(false);
                }));
    }

    /**
     * Load news from cache.
     */
    public void loadNews() {
        setLoading(true);
        setStatusMessage("Loading news...");
        logActivity("Loading news from cache for " + getSelectedTicker() + "...");

        apiService.getCachedNews(getSelectedTicker(), 50)
                .thenAccept(response -> Platform.runLater(() -> {
                    if (response.isSuccess()) {
                        setStatusMessage("Loaded news from cache");
                        logActivity("Loaded news from cache", LogLevel.INFO);
                    } else {
                        setStatusMessage("Failed to load news: " + response.getError());
                        logActivity("Failed: " + response.getError(), LogLevel.ERROR);
                    }
                    setLoading(false);
                }));
    }

    /**
     * Request AI analysis for selected ticker.
     */
    public void requestAnalysis() {
        if (getSelectedTicker() == null || getSelectedTicker().isEmpty()) {
            setStatusMessage("Please select a ticker");
            return;
        }

        setLoading(true);
        setStatusMessage("Requesting AI analysis...");
        logActivity("Starting AI analysis for " + getSelectedTicker() + " (" + getSelectedSector() + ") in "
                + getSelectedLanguage() + "...");

        apiService.requestAnalysis(List.of(getSelectedTicker()), getSelectedLanguage())
                .thenAccept(response -> Platform.runLater(() -> {
                    if (response.isSuccess()) {
                        setAnalysisResult(response.getBody());
                        setStatusMessage("Analysis complete");
                        logActivity("AI analysis completed successfully", LogLevel.INFO);
                    } else {
                        setStatusMessage("Analysis failed: " + response.getError());
                        setAnalysisResult("Error: " + response.getError());
                        logActivity("AI analysis FAILED: " + response.getError(), LogLevel.ERROR);
                    }
                    setLoading(false);
                }));
    }

    /**
     * Resolve fuzzy ticker name and auto-load sector.
     */
    public void resolveTicker() {
        String query = getSelectedTicker();
        if (query == null || query.isEmpty() || query.length() < 2)
            return;

        logActivity("Resolving ticker for: " + query);
        apiService.resolveTicker(query).thenAccept(response -> Platform.runLater(() -> {
            if (response.isSuccess()) {
                String body = response.getBody();

                // Extract symbol
                if (body.contains("\"symbol\":\"")) {
                    int start = body.indexOf("\"symbol\":\"") + 10;
                    int end = body.indexOf("\"", start);
                    String ticker = body.substring(start, end);
                    if (!ticker.isEmpty() && !ticker.equals(query)) {
                        setSelectedTicker(ticker);
                        logActivity("Resolved '" + query + "' to Ticker: " + ticker, LogLevel.INFO);
                    }
                }

                // Extract and auto-set sector
                if (body.contains("\"sector\":\"")) {
                    int sectorStart = body.indexOf("\"sector\":\"") + 10;
                    int sectorEnd = body.indexOf("\"", sectorStart);
                    String sector = body.substring(sectorStart, sectorEnd);
                    if (!sector.isEmpty()) {
                        setSelectedSector(sector);
                        logActivity("Auto-loaded sector: " + sector, LogLevel.INFO);
                    }
                }

                // Auto-load fundamentals for display
                loadFundamentals();
            }
        }));
    }

    /**
     * Resolve fuzzy sector name.
     */
    public void resolveSector() {
        String query = getSelectedSector();
        if (query == null || query.isEmpty() || query.length() < 2)
            return;

        apiService.resolveSector(query).thenAccept(response -> Platform.runLater(() -> {
            if (response.isSuccess()) {
                String body = response.getBody();
                if (body.contains("\"sector\":\"")) {
                    int start = body.indexOf("\"sector\":\"") + 10;
                    int end = body.indexOf("\"", start);
                    String sector = body.substring(start, end);
                    if (!sector.isEmpty() && !sector.equalsIgnoreCase(query)) {
                        setSelectedSector(sector);
                        logActivity("Resolved sector to: " + sector, LogLevel.INFO);
                    }
                }
            }
        }));
    }

    /**
     * Load fundamental data for a ticker from API.
     * Updates all fundamental properties for UI binding.
     */
    public void loadFundamentals() {
        String ticker = getSelectedTicker();
        if (ticker == null || ticker.isEmpty() || ticker.length() < 2)
            return;

        logActivity("Loading fundamentals for " + ticker + "...", LogLevel.DEBUG);

        apiService.getFundamentals(ticker).thenAccept(response -> Platform.runLater(() -> {
            if (response.isSuccess()) {
                String body = response.getBody();

                // Parse P/E Ratio
                peRatio.set(extractJsonNumber(body, "pe_ratio"));
                pegRatio.set(extractJsonNumber(body, "peg_ratio"));
                roe.set(extractJsonNumber(body, "roe") + "%");
                debtToEquity.set(extractJsonNumber(body, "debt_to_equity"));
                targetMean.set("$" + extractJsonNumber(body, "target_mean_price"));
                targetHigh.set("$" + extractJsonNumber(body, "target_high_price"));
                targetLow.set("$" + extractJsonNumber(body, "target_low_price"));
                recommendation.set(extractJsonString(body, "recommendation").toUpperCase());
                businessSummary.set(extractJsonString(body, "business_summary"));
                executiveSummary.set(extractJsonString(body, "executive_summary"));

                logActivity("Loaded fundamentals for " + ticker, LogLevel.INFO);
            } else {
                logActivity("Failed to load fundamentals: " + response.getError(), LogLevel.WARN);
                // Reset to defaults
                peRatio.set("-");
                pegRatio.set("-");
                roe.set("-");
                debtToEquity.set("-");
                targetMean.set("-");
                targetHigh.set("-");
                targetLow.set("-");
                recommendation.set("-");
                businessSummary.set("");
                executiveSummary.set("");
            }
        }));
    }

    private String extractJsonNumber(String json, String key) {
        try {
            String search = "\"" + key + "\":";
            int start = json.indexOf(search);
            if (start == -1)
                return "-";
            start += search.length();

            // Skip whitespace
            while (start < json.length() && Character.isWhitespace(json.charAt(start)))
                start++;

            // Handle null
            if (json.substring(start).startsWith("null"))
                return "N/A";

            // Find end of number
            int end = start;
            while (end < json.length()
                    && (Character.isDigit(json.charAt(end)) || json.charAt(end) == '.' || json.charAt(end) == '-')) {
                end++;
            }

            if (end > start) {
                double val = Double.parseDouble(json.substring(start, end));
                // Format based on value
                if (val >= 1000000000) {
                    return String.format("%.2fB", val / 1000000000);
                } else if (val >= 1000000) {
                    return String.format("%.2fM", val / 1000000);
                } else if (val >= 100) {
                    return String.format("%.2f", val);
                } else {
                    return String.format("%.2f", val);
                }
            }
        } catch (Exception e) {
            // ignore
        }
        return "-";
    }

    private String extractJsonString(String json, String key) {
        try {
            String search = "\"" + key + "\":\"";
            int start = json.indexOf(search);
            if (start == -1)
                return "";
            start += search.length();
            int end = json.indexOf("\"", start);
            if (end > start) {
                return json.substring(start, end);
            }
        } catch (Exception e) {
            // ignore
        }
        return "";
    }

    /**
     * Generate and export full HTML report.
     */
    public void exportHtmlReport() {
        // DEBUG: Log selected language to verify input capture
        try {
            String log = "DEBUG: exportHtmlReport called. Selected Language: '" + getSelectedLanguage() + "'\n";
            System.out.println(log);
            java.nio.file.Files.writeString(
                    java.nio.file.Path
                            .of("/Users/joern/Documents/News/Absci corp/stock-news-pro/debug_language_v2.txt"),
                    log,
                    java.nio.file.StandardOpenOption.CREATE, java.nio.file.StandardOpenOption.APPEND);
        } catch (Exception e) {
            e.printStackTrace();
        }
        if (getSelectedTicker() == null || getSelectedTicker().isEmpty())
            return;

        setLoading(true);
        setStatusMessage("Generating premium HTML report...");
        logActivity("Generating full report for " + getSelectedTicker() + "...");

        apiService.requestFullReport(List.of(getSelectedTicker()), getSelectedLanguage())
                .thenAccept(response -> Platform.runLater(() -> {
                    if (response.isSuccess()) {
                        String body = response.getBody();
                        if (body.contains("\"report_path\":\"")) {
                            int start = body.indexOf("\"report_path\":\"") + 15;
                            int end = body.indexOf("\"", start);
                            String path = body.substring(start, end);
                            setReportPath(path);
                            // Populate News Tracker with data from this report run
                            parseAndAddNews(body);

                            setStatusMessage("Report exported to: " + path);
                            logActivity("REPORT READY: " + path, LogLevel.INFO);

                            // Try to open it using system command (more reliable on macOS)
                            try {
                                String os = System.getProperty("os.name").toLowerCase();
                                ProcessBuilder pb;
                                if (os.contains("mac")) {
                                    pb = new ProcessBuilder("open", path);
                                } else if (os.contains("win")) {
                                    pb = new ProcessBuilder("cmd", "/c", "start", "", path);
                                } else {
                                    pb = new ProcessBuilder("xdg-open", path);
                                }
                                pb.start();
                                logActivity("Opened report in browser.", LogLevel.INFO);
                            } catch (Exception ex) {
                                logActivity("Could not open browser: " + ex.getMessage(), LogLevel.WARN);
                            }
                        }
                    } else {
                        setStatusMessage("Export failed: " + response.getError());
                        logActivity("Export FAILED: " + response.getError(), LogLevel.ERROR);
                    }
                    setLoading(false);
                }));
    }

    /**
     * Fetch news from external sources (RSS, yfinance).
     */
    public void fetchNews() {
        if (getSelectedTicker() == null || getSelectedTicker().isEmpty()) {
            setStatusMessage("Please select a ticker");
            return;
        }

        setLoading(true);
        setStatusMessage("Fetching news from external sources...");
        logActivity("Fetching news from yfinance/RSS for " + getSelectedTicker() + "...");

        apiService.fetchNews(List.of(getSelectedTicker()), 50)
                .thenAccept(response -> Platform.runLater(() -> {
                    if (response.isSuccess()) {
                        parseAndAddNews(response.getBody());
                        setStatusMessage("Fetched news successfully");
                        logActivity("Fetched " + newsItems.size() + " news items", LogLevel.INFO);
                    } else {
                        setStatusMessage("Fetch failed: " + response.getError());
                        logActivity("News fetch FAILED: " + response.getError(), LogLevel.ERROR);
                    }
                    setLoading(false);
                }));
    }

    /**
     * Parse JSON response and populate news items list.
     */
    private void parseAndAddNews(String json) {
        newsItems.clear();
        // Simple JSON parsing - in production use Jackson/Gson
        if (json == null || json.isEmpty())
            return;

        // Extract items array from response
        int itemsStart = json.indexOf("\"items\":");
        if (itemsStart == -1)
            return;

        // Find title fields and extract
        int pos = 0;
        while ((pos = json.indexOf("\"title\":", pos)) != -1) {
            int titleStart = json.indexOf("\"", pos + 8) + 1;
            int titleEnd = json.indexOf("\"", titleStart);
            if (titleStart > 0 && titleEnd > titleStart) {
                String title = json.substring(titleStart, titleEnd);

                // Find associated ticker
                int tickerPos = json.lastIndexOf("\"ticker\":", pos);
                String ticker = getSelectedTicker();
                if (tickerPos != -1 && tickerPos > pos - 200) {
                    int tStart = json.indexOf("\"", tickerPos + 9) + 1;
                    int tEnd = json.indexOf("\"", tStart);
                    if (tStart > 0 && tEnd > tStart) {
                        ticker = json.substring(tStart, tEnd);
                    }
                }

                // Find source
                int sourcePos = json.indexOf("\"source\":", pos);
                String source = "Unknown";
                if (sourcePos != -1 && sourcePos < pos + 300) {
                    int sStart = json.indexOf("\"", sourcePos + 9) + 1;
                    int sEnd = json.indexOf("\"", sStart);
                    if (sStart > 0 && sEnd > sStart) {
                        source = json.substring(sStart, sEnd);
                    }
                }

                // Find date/published
                String dateStr = "Just now";
                int datePos = json.indexOf("\"published\":", pos);
                if (datePos == -1)
                    datePos = json.indexOf("\"date\":", pos);

                if (datePos != -1 && datePos < pos + 400) {
                    int dStart = json.indexOf("\"", datePos + 10) + 1; // +10 covers "date": len 7 or "published": len
                                                                       // 12 approx
                    // safer to verify quote position
                    int colon = json.indexOf(":", datePos);
                    dStart = json.indexOf("\"", colon) + 1;
                    int dEnd = json.indexOf("\"", dStart);
                    if (dStart > 0 && dEnd > dStart) {
                        String rawDate = json.substring(dStart, dEnd);
                        if (rawDate.length() > 10)
                            dateStr = rawDate.substring(0, 10);
                        else
                            dateStr = rawDate;
                    }
                }

                newsItems.add(new NewsItem(ticker, title, source, dateStr));
            }
            pos = titleEnd > 0 ? titleEnd : pos + 1;
        }
    }

    // ==================== Property Getters/Setters ====================

    public boolean isConnected() {
        return connected.get();
    }

    public BooleanProperty connectedProperty() {
        return connected;
    }

    public void setConnected(boolean value) {
        connected.set(value);
    }

    public boolean isLoading() {
        return loading.get();
    }

    public BooleanProperty loadingProperty() {
        return loading;
    }

    public void setLoading(boolean value) {
        loading.set(value);
    }

    public String getStatusMessage() {
        return statusMessage.get();
    }

    public StringProperty statusMessageProperty() {
        return statusMessage;
    }

    public void setStatusMessage(String value) {
        statusMessage.set(value);
    }

    public String getAnalysisResult() {
        return analysisResult.get();
    }

    public StringProperty analysisResultProperty() {
        return analysisResult;
    }

    public void setAnalysisResult(String value) {
        analysisResult.set(value);
    }

    public String getSelectedTicker() {
        return selectedTicker.get();
    }

    public StringProperty selectedTickerProperty() {
        return selectedTicker;
    }

    public void setSelectedTicker(String value) {
        selectedTicker.set(value);
    }

    public String getSelectedSector() {
        return selectedSector.get();
    }

    public StringProperty selectedSectorProperty() {
        return selectedSector;
    }

    public void setSelectedSector(String value) {
        selectedSector.set(value);
    }

    public ObservableList<NewsItem> getNewsItems() {
        return newsItems;
    }

    public ObservableList<String> getActivityLog() {
        return activityLog;
    }

    public String getSelectedLanguage() {
        return selectedLanguage.get();
    }

    public StringProperty selectedLanguageProperty() {
        return selectedLanguage;
    }

    public void setSelectedLanguage(String value) {
        selectedLanguage.set(value);
    }

    public String getReportPath() {
        return reportPath.get();
    }

    public StringProperty reportPathProperty() {
        return reportPath;
    }

    public void setReportPath(String value) {
        reportPath.set(value);
    }

    // ==================== Fundamentals Property Getters ====================

    public StringProperty peRatioProperty() {
        return peRatio;
    }

    public StringProperty pegRatioProperty() {
        return pegRatio;
    }

    public StringProperty roeProperty() {
        return roe;
    }

    public StringProperty debtToEquityProperty() {
        return debtToEquity;
    }

    public StringProperty targetMeanProperty() {
        return targetMean;
    }

    public StringProperty targetHighProperty() {
        return targetHigh;
    }

    public StringProperty targetLowProperty() {
        return targetLow;
    }

    public StringProperty recommendationProperty() {
        return recommendation;
    }

    public StringProperty businessSummaryProperty() {
        return businessSummary;
    }

    public StringProperty executiveSummaryProperty() {
        return executiveSummary;
    }

    // ==================== Chart Property Getters ====================

    public StringProperty selectedChartPeriodProperty() {
        return selectedChartPeriod;
    }

    public ObservableList<PricePoint> getPriceHistory() {
        return priceHistory;
    }

    public StringProperty chartDateLabelProperty() {
        return chartDateLabel;
    }

    public BooleanProperty chartIsHistoricalProperty() {
        return chartIsHistorical;
    }

    public ObservableList<SectorNewsItem> getSectorNews() {
        return sectorNews;
    }

    // ==================== Chart Data Loading ====================

    /**
     * Load price history for the current ticker and selected period.
     */
    public void loadPriceHistory() {
        loadPriceHistory(selectedTicker.get(), selectedChartPeriod.get());
    }

    /**
     * Load price history for a specific ticker and period.
     */
    public void loadPriceHistory(String ticker, String period) {
        logActivity("Loading price history: " + ticker + " (" + period + ")", LogLevel.DEBUG);

        apiService.getPriceHistory(ticker, period)
                .thenAccept(response -> {
                    if (response.isSuccess()) {
                        Platform.runLater(() -> {
                            priceHistory.clear();

                            // Parse the JSON response
                            String body = response.getBody();

                            // Extract trading_date if present (for 24h mode)
                            String tradingDate = extractJsonString(body, "trading_date");
                            boolean isHistorical = body.contains("\"is_historical_day\":true");
                            chartDateLabel.set(tradingDate != null ? tradingDate : "");
                            chartIsHistorical.set(isHistorical);

                            // Parse prices array
                            int dataStart = body.indexOf("\"data\":[");
                            if (dataStart >= 0) {
                                int arrayStart = body.indexOf("[", dataStart);
                                int arrayEnd = body.lastIndexOf("]");
                                if (arrayStart >= 0 && arrayEnd > arrayStart) {
                                    String arrayContent = body.substring(arrayStart + 1, arrayEnd);
                                    // Split by },{ to get individual price objects
                                    String[] entries = arrayContent.split("\\},\\s*\\{");
                                    java.util.List<PricePoint> batch = new java.util.ArrayList<>();
                                    for (String entry : entries) {
                                        entry = entry.replace("{", "").replace("}", "");
                                        String date = extractJsonString(entry, "date");
                                        String time = extractJsonString(entry, "time");
                                        String closeStr = extractJsonNumber(entry, "close");
                                        Double close = null;
                                        try {
                                            if (closeStr != null && !closeStr.equals("-") && !closeStr.equals("N/A")) {
                                                close = Double.parseDouble(closeStr);
                                            }
                                        } catch (NumberFormatException e) {
                                            // Ignore parse errors
                                        }

                                        if (date != null && close != null) {
                                            batch.add(new PricePoint(date, close, time));
                                        }
                                    }
                                    priceHistory.addAll(batch);
                                    logActivity("Loaded " + batch.size() + " price points.", LogLevel.INFO);
                                }
                            }

                            logActivity("Loaded " + priceHistory.size() + " price points", LogLevel.DEBUG);
                            if (priceHistory.isEmpty()) {
                                generateFallbackData();
                            }
                        });
                    } else {
                        Platform.runLater(this::generateFallbackData);
                    }
                })
                .exceptionally(ex -> {
                    Platform.runLater(this::generateFallbackData);
                    logActivity("Failed to load prices: " + ex.getMessage(), LogLevel.ERROR);
                    return null;
                });
    }

    private void generateFallbackData() {
        logActivity("Generating dynamic fallback chart data...", LogLevel.WARN);
        priceHistory.clear();
        String period = selectedChartPeriod.get().toLowerCase();

        // Parameters for "Dynamic" feel
        int points = 30; // Default
        double volatility = 5.0;
        double trend = 0.5;

        switch (period) {
            case "24h":
                points = 24;
                volatility = 2.0;
                chartDateLabel.set("Mock 24h Data (Backend Unavailable)");
                break;
            case "1w":
                points = 7;
                volatility = 5.0;
                chartDateLabel.set("Mock 1w Data (Backend Unavailable)");
                break;
            case "1m":
                points = 30;
                volatility = 8.0;
                chartDateLabel.set("Mock 1m Data (Backend Unavailable)");
                break;
            case "3m":
                points = 90;
                volatility = 12.0;
                chartDateLabel.set("Mock 3m Data (Backend Unavailable)");
                break;
            case "1y":
                points = 52; // Weekly
                volatility = 20.0;
                chartDateLabel.set("Mock 1y Data (Backend Unavailable)");
                break;
            case "10y":
                points = 120; // Monthly
                volatility = 50.0;
                chartDateLabel.set("Mock 10y Data (Backend Unavailable)");
                break;
            default:
                chartDateLabel.set("Mock Data (Backend Unavailable)");
        }

        double price = 100.0 + (Math.random() * 20 - 10);
        for (int i = 0; i < points; i++) {
            // Random Walk + Trend + Sine Wave for "Stock-like" look
            double change = (Math.random() - 0.45) * volatility + trend; // Added trend
            double wave = Math.sin(i * 0.2) * (volatility / 2);
            price += change + (wave * 0.1);

            // Ensure price stays positive
            if (price < 10)
                price = 10;

            String label = period.equals("24h") ? (i + ":00") : "T-" + (points - i);
            priceHistory.add(new PricePoint(label, price));
        }
    }

    /**
     * Load sector news for the current sector.
     */
    public void loadSectorNews() {
        loadSectorNews(selectedSector.get());
    }

    /**
     * Load sector news for a specific sector.
     */
    public void loadSectorNews(String sector) {
        logActivity("Loading sector news: " + sector, LogLevel.DEBUG);

        apiService.getSectorNews(sector)
                .thenAccept(response -> {
                    if (response.isSuccess()) {
                        Platform.runLater(() -> {
                            sectorNews.clear();

                            String body = response.getBody();
                            // Parse news array
                            int newsStart = body.indexOf("\"news\":[");
                            if (newsStart >= 0) {
                                int arrayStart = body.indexOf("[", newsStart);
                                int arrayEnd = body.lastIndexOf("]");
                                if (arrayStart >= 0 && arrayEnd > arrayStart) {
                                    String arrayContent = body.substring(arrayStart + 1, arrayEnd);
                                    String[] entries = arrayContent.split("\\},\\s*\\{");
                                    for (String entry : entries) {
                                        entry = entry.replace("{", "").replace("}", "");
                                        String title = extractJsonString(entry, "title");
                                        String source = extractJsonString(entry, "source");
                                        String date = extractJsonString(entry, "date");

                                        if (title != null) {
                                            sectorNews.add(new SectorNewsItem(
                                                    title,
                                                    source != null ? source : "",
                                                    date != null ? date : ""));
                                        }
                                    }
                                }
                            }

                            logActivity("Loaded " + sectorNews.size() + " sector news items", LogLevel.DEBUG);
                        });
                    } else {
                        logActivity("Failed to load sector news: " + response.getError(), LogLevel.WARN);
                    }
                })
                .exceptionally(ex -> {
                    logActivity("Sector news error: " + ex.getMessage(), LogLevel.ERROR);
                    return null;
                });
    }

    /**
     * Simple news item model for list display.
     */
    public static class NewsItem {
        private final String ticker;
        private final String title;
        private final String source;
        private final String date;

        public NewsItem(String ticker, String title, String source, String date) {
            this.ticker = ticker;
            this.title = title;
            this.source = source;
            this.date = date;
        }

        public String getTicker() {
            return ticker;
        }

        public String getTitle() {
            return title;
        }

        public String getSource() {
            return source;
        }

        public String getDate() {
            return date;
        }

        @Override
        public String toString() {
            return "[" + ticker + "] " + title + " (" + source + ")";
        }
    }

    /**
     * Price point model for chart display.
     */
    public static class PricePoint {
        private final String date;
        private final double close;
        private final String time; // For intraday

        public PricePoint(String date, double close) {
            this.date = date;
            this.close = close;
            this.time = null;
        }

        public PricePoint(String date, double close, String time) {
            this.date = date;
            this.close = close;
            this.time = time;
        }

        public String getDate() {
            return date;
        }

        public double getClose() {
            return close;
        }

        public String getTime() {
            return time;
        }

        public String getLabel() {
            return time != null ? time : date;
        }
    }

    /**
     * Sector news item model for ticker display.
     */
    public static class SectorNewsItem {
        private final String title;
        private final String source;
        private final String date;

        public SectorNewsItem(String title, String source, String date) {
            this.title = title;
            this.source = source;
            this.date = date;
        }

        public String getTitle() {
            return title;
        }

        public String getSource() {
            return source;
        }

        public String getDate() {
            return date;
        }

        @Override
        public String toString() {
            return title + " (" + source + ")";
        }
    }
}
