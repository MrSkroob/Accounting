import sqlite3

# Run once to create database.


PERIODS_TABLE = ("CREATE TABLE Periods(PeriodID INTEGER PRIMARY KEY, "
                 "DateCreated TEXT, "
                 "StartDate TEXT, "
                 "EndDate TEXT, "
                 "Category TEXT, "
                 "ForecastRule TEXT, "
                 "Calculation REAL, "
                 "IsForecast INTEGER)")

PERIODS_HEADER = ["PeriodID", "DateCreated", "StartDate", "EndDate",
                  "Category", "ForecastRule", "Calculation", "IsForecast"]

PERIODS_TYPES = [
    "INTEGER",
    "TEXT",
    "TEXT",
    "TEXT",
    "TEXT",
    "TEXT",
    "REAL",
    "INTEGER"
]

PAYMENTS_TABLE = ("CREATE TABLE Payments("
                  "PaymentID TEXT PRIMARY KEY, "
                  "PeriodID INTEGER, "
                  "PayDate TEXT, "
                  "Net REAL,"
                  "Client TEXT,"
                  "FOREIGN KEY(PeriodID) REFERENCES Periods(PeriodID))")

PAYMENTS_HEADER = ["PaymentID", "PeriodID", "PayDate", "Net", "Client"]

PAYMENTS_TYPES = [
    "TEXT",
    "INTEGER",
    "TEXT",
    "REAL",
    "TEXT"
]

if __name__ == "__main__":
    connection = sqlite3.connect("../PE.db")
    cursor = connection.cursor()

    cursor.execute(PERIODS_TABLE)
    cursor.execute(PAYMENTS_TABLE)
    connection.commit()
