#ifndef API_CLIENT_H
#define API_CLIENT_H

#include <string>
#include <vector>
#include <functional>

namespace stocknews {

/**
 * HTTP Response structure
 */
struct HttpResponse {
    int status_code;
    std::string body;
    bool success;
    std::string error;
};

/**
 * News item for submission to AI Service
 */
struct NewsItemDTO {
    std::string ticker;
    std::string title;
    std::string source;
    std::string url;
    std::string published;  // ISO format
    std::string summary;
};

/**
 * Analysis result from AI Service
 */
struct AnalysisResult {
    std::string essay;
    std::string summary;
    std::string sentiment;
    std::vector<std::string> key_findings;
    bool success;
    std::string error;
};

/**
 * REST API Client for AI Service communication
 */
class ApiClient {
public:
    /**
     * Constructor
     * @param base_url Base URL of the AI Service (e.g., "http://localhost:8000")
     */
    explicit ApiClient(const std::string& base_url = "http://localhost:8000");
    
    ~ApiClient();
    
    /**
     * Check if AI Service is healthy
     * @return true if service is healthy
     */
    bool check_health();
    
    /**
     * Submit news items to AI Service
     * @param items Vector of news items
     * @param request_analysis If true, trigger analysis after submission
     * @return HttpResponse with result
     */
    HttpResponse submit_news(const std::vector<NewsItemDTO>& items, bool request_analysis = false);
    
    /**
     * Request AI analysis for tickers
     * @param tickers Vector of stock ticker symbols
     * @param language Output language (default: "German")
     * @return AnalysisResult with essay and findings
     */
    AnalysisResult request_analysis(const std::vector<std::string>& tickers, 
                                     const std::string& language = "German");
    
    /**
     * Get cached analysis for a ticker
     * @param ticker Stock ticker symbol
     * @return AnalysisResult (success=false if not cached)
     */
    AnalysisResult get_cached_analysis(const std::string& ticker);
    
    /**
     * Set connection timeout
     * @param timeout_seconds Timeout in seconds
     */
    void set_timeout(int timeout_seconds);
    
    /**
     * Get last error message
     */
    std::string get_last_error() const { return last_error_; }

private:
    std::string base_url_;
    int timeout_seconds_;
    std::string last_error_;
    
    // Internal HTTP methods
    HttpResponse http_get(const std::string& endpoint);
    HttpResponse http_post(const std::string& endpoint, const std::string& json_body);
    
    // JSON helpers
    std::string news_items_to_json(const std::vector<NewsItemDTO>& items, bool request_analysis);
    std::string analysis_request_to_json(const std::vector<std::string>& tickers, const std::string& language);
    AnalysisResult parse_analysis_response(const std::string& json);
};

} // namespace stocknews

#endif // API_CLIENT_H
