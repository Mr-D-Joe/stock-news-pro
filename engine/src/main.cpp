#include <iostream>
#include "dispatcher.h"

int main() {
    std::cout << "--- Stock News Data Engine (v2) ---" << std::endl;
    
    stocknews::Dispatcher dispatcher;

    std::cout << "Simulating real-time data stream..." << std::endl;
    dispatcher.dispatch_news("GOOGL", "Alphabet Reports Strong Q4 Results");
    dispatcher.dispatch_news("AMZN", "Amazon Expansion into Healthcare Gains Momentum");

    std::cout << "Engine cycle complete." << std::endl;
    
    return 0;
}
