package com.news_ai.stock.viewmodel;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

/**
 * Unit tests for MainViewModel.
 * Note: Tests without Mockito due to Java 25 compatibility issues.
 */
class MainViewModelTest {

    private MainViewModel viewModel;

    @BeforeEach
    void setUp() {
        // Use real ApiService for initialization tests
        viewModel = new MainViewModel();
    }

    @Test
    @DisplayName("ViewModel initializes with default values")
    void testDefaultInitialization() {
        assertFalse(viewModel.isConnected());
        assertFalse(viewModel.isLoading());
        assertEquals("Not connected", viewModel.getStatusMessage());
        assertEquals("", viewModel.getAnalysisResult());
        assertEquals("ABSI", viewModel.getSelectedTicker());
    }

    @Test
    @DisplayName("Sector property has default value")
    void testSectorProperty() {
        assertEquals("Biotech", viewModel.getSelectedSector());
        viewModel.setSelectedSector("Technology");
        assertEquals("Technology", viewModel.getSelectedSector());
    }

    @Test
    @DisplayName("Activity log starts with application started entry")
    void testActivityLog() {
        // Wait for Platform.runLater to complete (in tests it's immediate)
        assertFalse(viewModel.getActivityLog().isEmpty());
    }

    @Test
    @DisplayName("Connected property can be set and retrieved")
    void testConnectedProperty() {
        assertFalse(viewModel.isConnected());

        viewModel.setConnected(true);
        assertTrue(viewModel.isConnected());
        assertTrue(viewModel.connectedProperty().get());

        viewModel.setConnected(false);
        assertFalse(viewModel.isConnected());
    }

    @Test
    @DisplayName("Loading property can be set and retrieved")
    void testLoadingProperty() {
        assertFalse(viewModel.isLoading());

        viewModel.setLoading(true);
        assertTrue(viewModel.isLoading());
        assertTrue(viewModel.loadingProperty().get());

        viewModel.setLoading(false);
        assertFalse(viewModel.isLoading());
    }

    @Test
    @DisplayName("Status message property can be set and retrieved")
    void testStatusMessageProperty() {
        viewModel.setStatusMessage("Test status");
        assertEquals("Test status", viewModel.getStatusMessage());
        assertEquals("Test status", viewModel.statusMessageProperty().get());
    }

    @Test
    @DisplayName("Analysis result property can be set and retrieved")
    void testAnalysisResultProperty() {
        viewModel.setAnalysisResult("Test analysis content");
        assertEquals("Test analysis content", viewModel.getAnalysisResult());
        assertEquals("Test analysis content", viewModel.analysisResultProperty().get());
    }

    @Test
    @DisplayName("Selected ticker property can be set and retrieved")
    void testSelectedTickerProperty() {
        viewModel.setSelectedTicker("GOOGL");
        assertEquals("GOOGL", viewModel.getSelectedTicker());
        assertEquals("GOOGL", viewModel.selectedTickerProperty().get());
    }

    @Test
    @DisplayName("NewsItem model has correct properties")
    void testNewsItemModel() {
        MainViewModel.NewsItem item = new MainViewModel.NewsItem("AAPL", "Apple News", "Reuters", "2025-01-01");

        assertEquals("AAPL", item.getTicker());
        assertEquals("Apple News", item.getTitle());
        assertEquals("Reuters", item.getSource());
        assertEquals("2025-01-01", item.getDate());
    }

    @Test
    @DisplayName("NewsItem toString contains all properties")
    void testNewsItemToString() {
        MainViewModel.NewsItem item = new MainViewModel.NewsItem("TSLA", "Tesla Update", "Bloomberg", "Just now");
        String str = item.toString();

        assertTrue(str.contains("TSLA"));
        assertTrue(str.contains("Tesla Update"));
        assertTrue(str.contains("Bloomberg"));
    }

    @Test
    @DisplayName("News items list starts empty")
    void testNewsItemsListEmpty() {
        assertTrue(viewModel.getNewsItems().isEmpty());
    }

    @Test
    @DisplayName("Request analysis validates empty ticker")
    void testRequestAnalysisEmptyTicker() {
        viewModel.setSelectedTicker("");
        viewModel.requestAnalysis();

        assertEquals("Please select a ticker", viewModel.getStatusMessage());
    }

    @Test
    @DisplayName("Request analysis validates null ticker")
    void testRequestAnalysisNullTicker() {
        viewModel.setSelectedTicker(null);
        viewModel.requestAnalysis();

        assertEquals("Please select a ticker", viewModel.getStatusMessage());
    }
}
