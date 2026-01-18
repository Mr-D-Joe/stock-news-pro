package com.news_ai.stock.service;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;
import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.logging.Logger;

/**
 * HTTP Client Service for AI Service API communication.
 * Uses Java 11+ HttpClient for async HTTP requests.
 */
public class ApiService {

    private static final Logger logger = Logger.getLogger(ApiService.class.getName());

    private final HttpClient httpClient;
    private final String baseUrl;
    private final Duration timeout;

    /**
     * Create API service with default localhost configuration.
     */
    public ApiService() {
        this("http://localhost:8000", Duration.ofSeconds(30));
    }

    /**
     * Create API service with custom base URL.
     */
    public ApiService(String baseUrl, Duration timeout) {
        this.baseUrl = baseUrl;
        this.timeout = timeout;
        this.httpClient = HttpClient.newBuilder()
                .version(HttpClient.Version.HTTP_1_1)
                .connectTimeout(timeout)
                .build();
    }

    // ==================== Health Endpoints ====================

    /**
     * Check if AI Service is healthy.
     * 
     * @return CompletableFuture with true if service is alive
     */
    public CompletableFuture<Boolean> checkHealth() {
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(baseUrl + "/health/live"))
                .timeout(timeout)
                .GET()
                .build();

        return httpClient.sendAsync(request, HttpResponse.BodyHandlers.ofString())
                .thenApply(response -> {
                    boolean healthy = response.statusCode() == 200
                            && response.body().contains("\"alive\":true");
                    logger.info("Health check: " + (healthy ? "OK" : "FAILED"));
                    return healthy;
                })
                .exceptionally(ex -> {
                    logger.warning("Health check failed: " + ex.getMessage());
                    return false;
                });
    }

    /**
     * Get rate limit status from AI Service.
     * 
     * @return CompletableFuture with rate limit info as JSON
     */
    public CompletableFuture<ApiResponse> getRateLimitStatus() {
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(baseUrl + "/api/engine/rate-limit"))
                .timeout(Duration.ofSeconds(5))
                .GET()
                .build();

        return sendRequest(request);
    }

    /**
     * Get detailed health status.
     * 
     * @return CompletableFuture with JSON health response
     */
    public CompletableFuture<String> getHealthDetails() {
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(baseUrl + "/health/"))
                .timeout(timeout)
                .GET()
                .build();

        return httpClient.sendAsync(request, HttpResponse.BodyHandlers.ofString())
                .thenApply(HttpResponse::body)
                .exceptionally(ex -> "{\"error\": \"" + ex.getMessage() + "\"}");
    }

    // ==================== Engine API Endpoints ====================

    /**
     * Submit news items to the AI Service.
     * 
     * @param newsItemsJson JSON string with news items
     * @return CompletableFuture with API response
     */
    public CompletableFuture<ApiResponse> submitNews(String newsItemsJson) {
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(baseUrl + "/api/engine/news"))
                .timeout(timeout)
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(newsItemsJson))
                .build();

        return sendRequest(request);
    }

    /**
     * Get cached news from AI Service.
     * 
     * @param ticker Optional ticker filter
     * @param limit  Max items to return
     * @return CompletableFuture with cached news
     */
    public CompletableFuture<ApiResponse> getCachedNews(String ticker, int limit) {
        String url = baseUrl + "/api/engine/news?limit=" + limit;
        if (ticker != null && !ticker.isEmpty()) {
            url += "&ticker=" + ticker;
        }

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(url))
                .timeout(timeout)
                .GET()
                .build();

        return sendRequest(request);
    }

    /**
     * Request AI analysis for tickers.
     * 
     * @param tickers  List of stock tickers
     * @param language Output language
     * @return CompletableFuture with analysis result
     */
    public CompletableFuture<ApiResponse> requestAnalysis(List<String> tickers, String language) {
        StringBuilder json = new StringBuilder("{\"tickers\":[");
        for (int i = 0; i < tickers.size(); i++) {
            if (i > 0)
                json.append(",");
            json.append("\"").append(tickers.get(i)).append("\"");
        }
        json.append("],\"language\":\"").append(language).append("\"}");

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(baseUrl + "/api/engine/analyze"))
                .timeout(Duration.ofMinutes(2)) // Analysis takes longer
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(json.toString()))
                .build();

        return sendRequest(request);
    }

    /**
     * Get cached analysis for a ticker.
     * 
     * @param ticker Stock ticker
     * @return CompletableFuture with cached analysis
     */
    public CompletableFuture<ApiResponse> getCachedAnalysis(String ticker) {
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(baseUrl + "/api/engine/analyze/" + ticker))
                .timeout(timeout)
                .GET()
                .build();

        return sendRequest(request);
    }

    /**
     * Resolve fuzzy stock name to ticker.
     * 
     * @param query Search query (e.g. "Mercedes")
     * @return CompletableFuture with resolution JSON
     */
    public CompletableFuture<ApiResponse> resolveTicker(String query) {
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(baseUrl + "/resolve/ticker?query="
                        + java.net.URLEncoder.encode(query, java.nio.charset.StandardCharsets.UTF_8)))
                .timeout(timeout)
                .GET()
                .build();

        return sendRequest(request);
    }

    /**
     * Resolve fuzzy sector name.
     * 
     * @param query Search query (e.g. "Auto")
     * @return CompletableFuture with sector JSON
     */
    public CompletableFuture<ApiResponse> resolveSector(String query) {
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(baseUrl + "/resolve/sector?query="
                        + java.net.URLEncoder.encode(query, java.nio.charset.StandardCharsets.UTF_8)))
                .timeout(timeout)
                .GET()
                .build();

        return sendRequest(request);
    }

    /**
     * Get fundamental data for a stock (P/E, ROE, targets, etc.).
     * 
     * @param ticker Stock ticker
     * @return CompletableFuture with fundamentals JSON
     */
    public CompletableFuture<ApiResponse> getFundamentals(String ticker) {
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(baseUrl + "/api/fundamentals?ticker="
                        + java.net.URLEncoder.encode(ticker, java.nio.charset.StandardCharsets.UTF_8)))
                .timeout(timeout)
                .GET()
                .build();

        return sendRequest(request);
    }

    /**
     * Get price history for a stock.
     * 
     * @param ticker Stock ticker
     * @param period Time period: 24h, 1wk, 1mo, 3mo, 1y, 10y
     * @return CompletableFuture with price data JSON
     */
    public CompletableFuture<ApiResponse> getPriceHistory(String ticker, String period) {
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(baseUrl + "/api/price_history?ticker="
                        + java.net.URLEncoder.encode(ticker, java.nio.charset.StandardCharsets.UTF_8)
                        + "&period=" + java.net.URLEncoder.encode(period, java.nio.charset.StandardCharsets.UTF_8)))
                .timeout(timeout)
                .GET()
                .build();

        return sendRequest(request);
    }

    /**
     * Get sector-wide news headlines.
     * 
     * @param sector Sector name (e.g. "Technology", "Healthcare")
     * @return CompletableFuture with sector news JSON
     */
    public CompletableFuture<ApiResponse> getSectorNews(String sector) {
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(baseUrl + "/api/sector_news?sector="
                        + java.net.URLEncoder.encode(sector, java.nio.charset.StandardCharsets.UTF_8)))
                .timeout(timeout)
                .GET()
                .build();

        return sendRequest(request);
    }

    /**
     * Request a full HTML report with charts and historical analysis.
     * 
     * @param tickers  List of stock tickers (usually just one)
     * @param language Output language
     * @return CompletableFuture with report info
     */
    public CompletableFuture<ApiResponse> requestFullReport(List<String> tickers, String language) {
        StringBuilder json = new StringBuilder("{\"query_stocks\":[");
        for (int i = 0; i < tickers.size(); i++) {
            if (i > 0)
                json.append(",");
            json.append("\"").append(tickers.get(i)).append("\"");
        }
        json.append("]}"); // Remove language from body, strictly query param

        String encodedLang = "German";
        try {
            encodedLang = java.net.URLEncoder.encode(language, java.nio.charset.StandardCharsets.UTF_8);
        } catch (Exception e) {
            e.printStackTrace();
        }

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(baseUrl + "/analyze/full_report?language=" + encodedLang))
                .timeout(Duration.ofMinutes(5)) // Full report takes time
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(json.toString()))
                .build();

        return sendRequest(request);
    }

    /**
     * Fetch news from external sources (RSS, yfinance).
     * 
     * @param tickers      List of stock tickers
     * @param maxPerTicker Max news items per ticker
     * @return CompletableFuture with fetched news
     */
    public CompletableFuture<ApiResponse> fetchNews(List<String> tickers, int maxPerTicker) {
        StringBuilder json = new StringBuilder("{\"tickers\":[");
        for (int i = 0; i < tickers.size(); i++) {
            if (i > 0)
                json.append(",");
            json.append("\"").append(tickers.get(i)).append("\"");
        }
        json.append("],\"max_per_ticker\":").append(maxPerTicker).append("}");

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(baseUrl + "/api/engine/fetch"))
                .timeout(Duration.ofMinutes(1)) // Fetching takes time
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(json.toString()))
                .build();

        return sendRequest(request);
    }

    // ==================== Helper Methods ====================

    private CompletableFuture<ApiResponse> sendRequest(HttpRequest request) {
        return httpClient.sendAsync(request, HttpResponse.BodyHandlers.ofString())
                .thenApply(response -> {
                    boolean success = response.statusCode() >= 200 && response.statusCode() < 300;
                    String error = null;

                    if (!success) {
                        // Try to extract detail from JSON error
                        // Format usually: {"detail": "Rate limit exceeded: ..."}
                        String body = response.body();
                        if (body != null && body.contains("\"detail\":")) {
                            try {
                                int start = body.indexOf("\"detail\":") + 9;
                                int valStart = body.indexOf("\"", start) + 1;
                                int valEnd = body.indexOf("\"", valStart);
                                if (valStart > 0 && valEnd > valStart) {
                                    error = body.substring(valStart, valEnd);
                                } else {
                                    error = "HTTP " + response.statusCode();
                                }
                            } catch (Exception e) {
                                error = "HTTP " + response.statusCode() + " (parse error)";
                            }
                        } else {
                            error = "HTTP " + response.statusCode();
                        }
                    }

                    return new ApiResponse(
                            response.statusCode(),
                            response.body(),
                            success,
                            error);
                })
                .exceptionally(ex -> new ApiResponse(
                        0,
                        null,
                        false,
                        ex.getMessage()));
    }

    /**
     * API Response wrapper.
     */
    public static class ApiResponse {
        private final int statusCode;
        private final String body;
        private final boolean success;
        private final String error;

        public ApiResponse(int statusCode, String body, boolean success, String error) {
            this.statusCode = statusCode;
            this.body = body;
            this.success = success;
            this.error = error;
        }

        public int getStatusCode() {
            return statusCode;
        }

        public String getBody() {
            return body;
        }

        public boolean isSuccess() {
            return success;
        }

        public String getError() {
            return error;
        }

        @Override
        public String toString() {
            return "ApiResponse{status=" + statusCode + ", success=" + success +
                    (error != null ? ", error=" + error : "") + "}";
        }
    }
}
