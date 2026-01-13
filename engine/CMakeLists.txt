cmake_minimum_required(VERSION 3.10)
project(StockNewsEngine VERSION 1.0)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Source files
set(SOURCES
    src/main.cpp
    src/database.c
)

add_executable(news_engine ${SOURCES})

# Future: Add gRPC/Protobuf dependencies
