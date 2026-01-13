cmake_minimum_required(VERSION 3.10)
project(StockNewsEngine VERSION 1.0)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Source files
set(SOURCES
    src/main.cpp
    src/database.c
)

find_package(SQLite3 REQUIRED)
add_executable(news_engine ${SOURCES})
target_link_libraries(news_engine SQLite3::SQLite3)

# Future: Add gRPC/Protobuf dependencies
