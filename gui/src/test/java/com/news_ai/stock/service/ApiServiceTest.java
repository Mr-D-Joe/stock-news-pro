package com.news_ai.stock.service;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

import java.time.Duration;
import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.TimeUnit;

/**
 * Unit tests for ApiService.
 */
class ApiServiceTest {

    private ApiService apiService;

    @BeforeEach
    void setUp() {
        // Use non-existent port for offline tests
        apiService = new ApiService("http://localhost:19999", Duration.ofSeconds(2));
    }

    @Test
    @DisplayName("ApiService can be constructed with defaults")
    void testDefaultConstruction() {
        ApiService defaultService = new ApiService();
        assertNotNull(defaultService);
    }

    @Test
    @DisplayName("ApiService can be constructed with custom URL")
    void testCustomConstruction() {
        ApiService customService = new ApiService("http://custom:9000", Duration.ofSeconds(10));
        assertNotNull(customService);
    }

    @Test
    @DisplayName("Health check returns false when service is offline")
    void testHealthCheckOffline() throws Exception {
        CompletableFuture<Boolean> future = apiService.checkHealth();
        Boolean result = future.get(5, TimeUnit.SECONDS);
        assertFalse(result, "Health check should return false when service is offline");
    }

    @Test
    @DisplayName("Get health details returns error when offline")
    void testHealthDetailsOffline() throws Exception {
        CompletableFuture<String> future = apiService.getHealthDetails();
        String result = future.get(5, TimeUnit.SECONDS);
        assertTrue(result.contains("error"), "Should contain error message");
    }

    @Test
    @DisplayName("Submit news returns failure when offline")
    void testSubmitNewsOffline() throws Exception {
        String json = "{\"items\":[{\"ticker\":\"TEST\",\"title\":\"Test\",\"source\":\"Test\"}],\"request_analysis\":false}";
        CompletableFuture<ApiService.ApiResponse> future = apiService.submitNews(json);
        ApiService.ApiResponse response = future.get(5, TimeUnit.SECONDS);
        assertFalse(response.isSuccess(), "Submit should fail when offline");
    }

    @Test
    @DisplayName("Get cached news returns failure when offline")
    void testGetCachedNewsOffline() throws Exception {
        CompletableFuture<ApiService.ApiResponse> future = apiService.getCachedNews("AAPL", 10);
        ApiService.ApiResponse response = future.get(5, TimeUnit.SECONDS);
        assertFalse(response.isSuccess());
    }

    @Test
    @DisplayName("Request analysis returns failure when offline")
    void testRequestAnalysisOffline() throws Exception {
        CompletableFuture<ApiService.ApiResponse> future = apiService.requestAnalysis(List.of("AAPL"), "German");
        ApiService.ApiResponse response = future.get(5, TimeUnit.SECONDS);
        assertFalse(response.isSuccess());
    }

    @Test
    @DisplayName("Get cached analysis returns failure when offline")
    void testGetCachedAnalysisOffline() throws Exception {
        CompletableFuture<ApiService.ApiResponse> future = apiService.getCachedAnalysis("AAPL");
        ApiService.ApiResponse response = future.get(5, TimeUnit.SECONDS);
        assertFalse(response.isSuccess());
    }

    @Test
    @DisplayName("ApiResponse has correct properties")
    void testApiResponseProperties() {
        ApiService.ApiResponse response = new ApiService.ApiResponse(200, "{}", true, null);

        assertEquals(200, response.getStatusCode());
        assertEquals("{}", response.getBody());
        assertTrue(response.isSuccess());
        assertNull(response.getError());
    }

    @Test
    @DisplayName("ApiResponse with error has correct properties")
    void testApiResponseWithError() {
        ApiService.ApiResponse response = new ApiService.ApiResponse(0, null, false, "Connection refused");

        assertEquals(0, response.getStatusCode());
        assertNull(response.getBody());
        assertFalse(response.isSuccess());
        assertEquals("Connection refused", response.getError());
    }

    @Test
    @DisplayName("ApiResponse toString is formatted correctly")
    void testApiResponseToString() {
        ApiService.ApiResponse success = new ApiService.ApiResponse(200, "{}", true, null);
        assertTrue(success.toString().contains("status=200"));
        assertTrue(success.toString().contains("success=true"));

        ApiService.ApiResponse error = new ApiService.ApiResponse(0, null, false, "Error");
        assertTrue(error.toString().contains("error=Error"));
    }
}
