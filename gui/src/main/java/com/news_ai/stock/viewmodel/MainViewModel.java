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
}
