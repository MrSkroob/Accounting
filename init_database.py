import sqlite3
# Run once to create database.

if __name__ == "__main__":
    connection = sqlite3.connect("PE.db")
    cursor = connection.cursor()

    cursor.execute("CREATE TABLE Periods("
                   "PeriodID INTEGER PRIMARY KEY, "
                   "DateCreated, "
                   "StartDate NUMERIC, "
                   "EndDate NUMERIC, "
                   "Category TEXT, "
                   "ForecastRule TEXT, "
                   "Calculation REAL, "
                   "IsForecast INTEGER)")
    cursor.execute("CREATE TABLE Payments("
                   "PaymentID INTEGER PRIMARY KEY, "
                   "PeriodID, "
                   "DateCreated NUMERIC, "
                   "Net REAL,"
                   "FOREIGN KEY(PeriodID) REFERENCES Periods(PeriodID))")
    connection.commit()
