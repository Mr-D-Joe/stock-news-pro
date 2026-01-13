#include <iostream>
#include "database.h"

int main() {
    std::cout << "--- Stock News Data Engine ---" << std::endl;
    
    if (!db_init("stock_news.db")) {
        return 1;
    }

    std::cout << "Storing test data..." << std::endl;
    db_store_news("AAPL", "Apple launches new AI chip", "2026-01-13");
    db_store_news("TSLA", "Tesla production reaches record high", "2026-01-13");

    db_close();
    std::cout << "Engine cycle complete." << std::endl;
    
    return 0;
}
