#ifndef DISPATCHER_H
#define DISPATCHER_H

#include <string>
#include <vector>

namespace stocknews {

class Dispatcher {
public:
    Dispatcher();
    ~Dispatcher();

    // Process a new batch of news
    void dispatch_news(const std::string& ticker, const std::string& title);

private:
    void init_systems();
    void shutdown_systems();
};

} // namespace stocknews

#endif // DISPATCHER_H
