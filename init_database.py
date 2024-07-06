import sqlite3
# Run once to create database.

if __name__ == "main":
    connection = sqlite3.connect("PE.db")
    cursor = connection.cursor()

    cursor.execute("CREATE TABLE periods("
                   "PeriodID PRIMARY KEY, "
                   "date_created, "
                   "start_date NUMERIC, "
                   "end_date NUMERIC, "
                   "category TEXT, "
                   "forecast_rule TEXT, "
                   "calculation REAL, "
                   "is_forecast INTEGER)")
    cursor.execute("CREATE TABLE payments("
                   "PaymentID PRIMARY KEY, "
                   "PeriodID, "
                   "date_created NUMERIC, "
                   "net REAL,"
                   "FOREIGN KEY(PeriodID) REFERENCES periods(PeriodID))")
    connection.commit()
