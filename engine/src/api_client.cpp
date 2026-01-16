/**
 * REST API Client implementation for AI Service communication
 * 
 * Uses libcurl for HTTP requests.
 * Compile with: -lcurl
 */

#include "api_client.h"
#include <curl/curl.h>
#include <sstream>
#include <iostream>
#include <cstring>

namespace stocknews {

// Callback for libcurl to write response data
static size_t write_callback(void* contents, size_t size, size_t nmemb, std::string* userp) {
    size_t total_size = size * nmemb;
    userp->append(static_cast<char*>(contents), total_size);
    return total_size;
}

ApiClient::ApiClient(const std::string& base_url)
    : base_url_(base_url), timeout_seconds_(30) {
    // Initialize libcurl globally (should be called once per application)
    static bool curl_initialized = false;
    if (!curl_initialized) {
        curl_global_init(CURL_GLOBAL_ALL);
        curl_initialized = true;
    }
}

ApiClient::~ApiClient() {
    // Note: curl_global_cleanup() should be called at app exit, not here
}

void ApiClient::set_timeout(int timeout_seconds) {
    timeout_seconds_ = timeout_seconds;
}

HttpResponse ApiClient::http_get(const std::string& endpoint) {
    HttpResponse response{0, "", false, ""};
    
    CURL* curl = curl_easy_init();
    if (!curl) {
        response.error = "Failed to initialize CURL";
        last_error_ = response.error;
        return response;
    }
    
    std::string url = base_url_ + endpoint;
    std::string response_body;
    
    curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &response_body);
    curl_easy_setopt(curl, CURLOPT_TIMEOUT, timeout_seconds_);
    curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);
    
    CURLcode res = curl_easy_perform(curl);
    
    if (res != CURLE_OK) {
        response.error = curl_easy_strerror(res);
        last_error_ = response.error;
    } else {
        long http_code = 0;
        curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &http_code);
        response.status_code = static_cast<int>(http_code);
        response.body = response_body;
        response.success = (http_code >= 200 && http_code < 300);
    }
    
    curl_easy_cleanup(curl);
    return response;
}

HttpResponse ApiClient::http_post(const std::string& endpoint, const std::string& json_body) {
    HttpResponse response{0, "", false, ""};
    
    CURL* curl = curl_easy_init();
    if (!curl) {
        response.error = "Failed to initialize CURL";
        last_error_ = response.error;
        return response;
    }
    
    std::string url = base_url_ + endpoint;
    std::string response_body;
    
    struct curl_slist* headers = nullptr;
    headers = curl_slist_append(headers, "Content-Type: application/json");
    
    curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
    curl_easy_setopt(curl, CURLOPT_POSTFIELDS, json_body.c_str());
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &response_body);
    curl_easy_setopt(curl, CURLOPT_TIMEOUT, timeout_seconds_);
    
    CURLcode res = curl_easy_perform(curl);
    
    if (res != CURLE_OK) {
        response.error = curl_easy_strerror(res);
        last_error_ = response.error;
    } else {
        long http_code = 0;
        curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &http_code);
        response.status_code = static_cast<int>(http_code);
        response.body = response_body;
        response.success = (http_code >= 200 && http_code < 300);
    }
    
    curl_slist_free_all(headers);
    curl_easy_cleanup(curl);
    return response;
}

bool ApiClient::check_health() {
    HttpResponse resp = http_get("/health/live");
    return resp.success && resp.body.find("\"alive\":true") != std::string::npos;
}

std::string ApiClient::news_items_to_json(const std::vector<NewsItemDTO>& items, bool request_analysis) {
    std::ostringstream json;
    json << "{\"items\":[";
    
    for (size_t i = 0; i < items.size(); ++i) {
        const auto& item = items[i];
        if (i > 0) json << ",";
        json << "{"
             << "\"ticker\":\"" << item.ticker << "\","
             << "\"title\":\"" << item.title << "\","
             << "\"source\":\"" << item.source << "\"";
        
        if (!item.url.empty()) {
            json << ",\"url\":\"" << item.url << "\"";
        }
        if (!item.summary.empty()) {
            json << ",\"summary\":\"" << item.summary << "\"";
        }
        json << "}";
    }
    
    json << "],\"request_analysis\":" << (request_analysis ? "true" : "false") << "}";
    return json.str();
}

HttpResponse ApiClient::submit_news(const std::vector<NewsItemDTO>& items, bool request_analysis) {
    std::string json = news_items_to_json(items, request_analysis);
    return http_post("/api/engine/news", json);
}

std::string ApiClient::analysis_request_to_json(const std::vector<std::string>& tickers, const std::string& language) {
    std::ostringstream json;
    json << "{\"tickers\":[";
    
    for (size_t i = 0; i < tickers.size(); ++i) {
        if (i > 0) json << ",";
        json << "\"" << tickers[i] << "\"";
    }
    
    json << "],\"language\":\"" << language << "\"}";
    return json.str();
}

// Simple JSON value extractor (for production, use a proper JSON library like nlohmann/json)
static std::string extract_json_string(const std::string& json, const std::string& key) {
    std::string search = "\"" + key + "\":\"";
    size_t start = json.find(search);
    if (start == std::string::npos) return "";
    
    start += search.length();
    size_t end = json.find("\"", start);
    if (end == std::string::npos) return "";
    
    return json.substr(start, end - start);
}

AnalysisResult ApiClient::parse_analysis_response(const std::string& json) {
    AnalysisResult result;
    result.success = true;
    
    result.essay = extract_json_string(json, "essay");
    result.summary = extract_json_string(json, "summary");
    result.sentiment = extract_json_string(json, "sentiment");
    
    // Extract key_findings array (simplified parsing)
    size_t findings_start = json.find("\"key_findings\":[");
    if (findings_start != std::string::npos) {
        size_t array_start = json.find("[", findings_start);
        size_t array_end = json.find("]", array_start);
        if (array_start != std::string::npos && array_end != std::string::npos) {
            std::string findings_str = json.substr(array_start + 1, array_end - array_start - 1);
            // Parse individual strings (simplified)
            size_t pos = 0;
            while ((pos = findings_str.find("\"", pos)) != std::string::npos) {
                size_t end = findings_str.find("\"", pos + 1);
                if (end != std::string::npos) {
                    result.key_findings.push_back(findings_str.substr(pos + 1, end - pos - 1));
                    pos = end + 1;
                } else {
                    break;
                }
            }
        }
    }
    
    return result;
}

AnalysisResult ApiClient::request_analysis(const std::vector<std::string>& tickers, const std::string& language) {
    AnalysisResult result;
    result.success = false;
    
    std::string json = analysis_request_to_json(tickers, language);
    HttpResponse resp = http_post("/api/engine/analyze", json);
    
    if (!resp.success) {
        result.error = resp.error.empty() ? "HTTP request failed" : resp.error;
        last_error_ = result.error;
        return result;
    }
    
    return parse_analysis_response(resp.body);
}

AnalysisResult ApiClient::get_cached_analysis(const std::string& ticker) {
    AnalysisResult result;
    result.success = false;
    
    HttpResponse resp = http_get("/api/engine/analyze/" + ticker);
    
    if (!resp.success) {
        result.error = "Analysis not cached";
        return result;
    }
    
    return parse_analysis_response(resp.body);
}

} // namespace stocknews
