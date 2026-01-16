/**
 * Unit tests for API Client
 * 
 * Tests API client functionality without requiring a running server.
 * Compile: cmake --build . --target test_api_client
 * Run: ./test_api_client
 */

#include "api_client.h"
#include <iostream>
#include <cassert>

using namespace stocknews;

// Test counter
static int tests_passed = 0;
static int tests_failed = 0;

#define TEST(name) \
    std::cout << "Test: " << #name << "... "; \
    try { test_##name(); tests_passed++; std::cout << "PASSED\n"; } \
    catch (const std::exception& e) { tests_failed++; std::cout << "FAILED: " << e.what() << "\n"; }

#define ASSERT(condition) \
    if (!(condition)) throw std::runtime_error("Assertion failed: " #condition);

// ==================== Test Cases ====================

void test_client_construction() {
    ApiClient client("http://localhost:8000");
    ASSERT(client.get_last_error().empty());
}

void test_client_custom_url() {
    ApiClient client("http://custom-host:9000");
    ASSERT(client.get_last_error().empty());
}

void test_timeout_setting() {
    ApiClient client;
    client.set_timeout(60);
    // No direct way to verify, but should not throw
    ASSERT(client.get_last_error().empty());
}

void test_news_dto_creation() {
    NewsItemDTO item;
    item.ticker = "AAPL";
    item.title = "Test News";
    item.source = "TestSource";
    item.url = "http://example.com";
    item.summary = "Test summary";
    
    ASSERT(item.ticker == "AAPL");
    ASSERT(item.title == "Test News");
}

void test_analysis_result_structure() {
    AnalysisResult result;
    result.success = true;
    result.essay = "Test essay";
    result.summary = "Test summary";
    result.sentiment = "positive";
    result.key_findings.push_back("Finding 1");
    result.key_findings.push_back("Finding 2");
    
    ASSERT(result.success);
    ASSERT(result.key_findings.size() == 2);
}

void test_http_response_structure() {
    HttpResponse response;
    response.status_code = 200;
    response.body = "{\"test\": \"data\"}";
    response.success = true;
    response.error = "";
    
    ASSERT(response.success);
    ASSERT(response.status_code == 200);
}

// Note: These tests require a running AI Service
void test_health_check_offline() {
    ApiClient client("http://localhost:19999");  // Non-existent port
    client.set_timeout(2);  // Short timeout
    
    bool healthy = client.check_health();
    ASSERT(!healthy);  // Should fail since no server is running
}

void test_submit_news_offline() {
    ApiClient client("http://localhost:19999");
    client.set_timeout(2);
    
    std::vector<NewsItemDTO> items;
    NewsItemDTO item;
    item.ticker = "TEST";
    item.title = "Test Title";
    item.source = "TestSource";
    items.push_back(item);
    
    HttpResponse resp = client.submit_news(items, false);
    ASSERT(!resp.success);  // Should fail since no server
}

// ==================== Main ====================

int main() {
    std::cout << "\n========== API Client Unit Tests ==========\n\n";
    
    TEST(client_construction);
    TEST(client_custom_url);
    TEST(timeout_setting);
    TEST(news_dto_creation);
    TEST(analysis_result_structure);
    TEST(http_response_structure);
    TEST(health_check_offline);
    TEST(submit_news_offline);
    
    std::cout << "\n==========================================\n";
    std::cout << "Tests passed: " << tests_passed << "\n";
    std::cout << "Tests failed: " << tests_failed << "\n";
    std::cout << "==========================================\n\n";
    
    return tests_failed > 0 ? 1 : 0;
}
