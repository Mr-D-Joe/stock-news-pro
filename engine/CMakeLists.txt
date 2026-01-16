cmake_minimum_required(VERSION 3.10)
project(StockNewsEngine VERSION 1.0)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find required packages
find_package(SQLite3 REQUIRED)
find_package(CURL REQUIRED)

# Source files
set(SOURCES
    src/main.cpp
    src/database.c
    src/dispatcher.cpp
    src/api_client.cpp
)

# Main executable
add_executable(news_engine ${SOURCES})

target_include_directories(news_engine PRIVATE 
    ${CURL_INCLUDE_DIRS}
)

target_link_libraries(news_engine 
    SQLite3::SQLite3
    ${CURL_LIBRARIES}
)

# ==================== Tests ====================
enable_testing()

# Test executable for API Client
add_executable(test_api_client
    tests/test_api_client.cpp
    src/api_client.cpp
)

target_include_directories(test_api_client PRIVATE 
    ${CMAKE_SOURCE_DIR}/src
    ${CURL_INCLUDE_DIRS}
)

target_link_libraries(test_api_client 
    ${CURL_LIBRARIES}
)

add_test(NAME ApiClientTest COMMAND test_api_client)

# Print configuration info
message(STATUS "SQLite3 found: ${SQLite3_LIBRARIES}")
message(STATUS "CURL found: ${CURL_LIBRARIES}")
