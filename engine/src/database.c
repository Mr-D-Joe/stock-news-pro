#include "database.h"
#include <stdio.h>
#include <sqlite3.h>

static sqlite3 *db = NULL;

bool db_init(const char* db_path) {
    int rc = sqlite3_open(db_path, &db);
    if (rc) {
        fprintf(stderr, "Can't open database: %s\n", sqlite3_errmsg(db));
        return false;
    }

    const char *sql = "CREATE TABLE IF NOT EXISTS news_impact ("
                      "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                      "ticker TEXT NOT NULL,"
                      "title TEXT,"
                      "category TEXT,"
                      "relevance REAL,"
                      "date TEXT);";

    char *err_msg = 0;
    rc = sqlite3_exec(db, sql, 0, 0, &err_msg);
    if (rc != SQLITE_OK) {
        fprintf(stderr, "SQL error: %s\n", err_msg);
        sqlite3_free(err_msg);
        return false;
    }

    printf("Database initialized successfully at: %s\n", db_path);
    return true;
}

bool db_store_news(const char* ticker, const char* title, const char* date) {
    const char *sql = "INSERT INTO news_impact (ticker, title, date) VALUES (?, ?, ?);";
    sqlite3_stmt *res;

    int rc = sqlite3_prepare_v2(db, sql, -1, &res, 0);
    if (rc != SQLITE_OK) return false;

    sqlite3_bind_text(res, 1, ticker, -1, SQLITE_STATIC);
    sqlite3_bind_text(res, 2, title, -1, SQLITE_STATIC);
    sqlite3_bind_text(res, 3, date, -1, SQLITE_STATIC);

    rc = sqlite3_step(res);
    sqlite3_finalize(res);

    return rc == SQLITE_DONE;
}

void db_close() {
    if (db) {
        sqlite3_close(db);
        printf("Database connection closed.\n");
    }
}
