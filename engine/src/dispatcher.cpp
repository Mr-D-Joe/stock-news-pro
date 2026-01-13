#include "dispatcher.h"
#include "database.h"
#include <iostream>
#include <ctime>

namespace stocknews {

Dispatcher::Dispatcher() {
    init_systems();
}

Dispatcher::~Dispatcher() {
    shutdown_systems();
}

void Dispatcher::init_systems() {
    db_init("stock_news.db");
    std::cout << "[Dispatcher] Systems initialized." << std::endl;
}

void Dispatcher::shutdown_systems() {
    db_close();
    std::cout << "[Dispatcher] Systems shut down." << std::endl;
}

void Dispatcher::dispatch_news(const std::string& ticker, const std::string& title) {
    std::time_t now = std::time(nullptr);
    char buf[11];
    std::strftime(buf, sizeof(buf), "%Y-%m-%d", std::localtime(&now));
    
    std::cout << "[Dispatcher] Routing news: " << ticker << std::endl;
    db_store_news(ticker.c_str(), title.c_str(), buf);
}

} // namespace stocknews
