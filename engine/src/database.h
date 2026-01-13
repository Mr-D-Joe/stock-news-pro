#ifndef DATABASE_H
#define DATABASE_H

#ifdef __cplusplus
extern "C" {
#endif

#include <stdbool.h>

// Initialize the database system
bool db_init(const char* db_path);

// Store a news item efficiently
bool db_store_news(const char* ticker, const char* title, const char* date);

// Close the database
void db_close();

#ifdef __cplusplus
}
#endif

#endif // DATABASE_H
