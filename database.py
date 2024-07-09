import sqlite3
import datetime
from datatypes import *


connection = sqlite3.connect("PE.db")
cursor = connection.cursor()


def string_to_date(date_str: str) -> date:
    return datetime.datetime.strptime(date_str, "%d/%m/%Y").date()


def add_period_entry(period_entry: PeriodEntry):
    periods_command = ("INSERT INTO Periods(DateCreated, StartDate, EndDate, Category, ForecastRule, Calculation,"
                       " IsForecast)"
                       "VALUES(?, ?, ?, ?, ?, ?, ?)")

    cursor.execute(periods_command, (datetime.date.today().strftime("%d/%m/%Y"),
                                     period_entry.work_start,
                                     period_entry.work_end,
                                     period_entry.category,
                                     0,
                                     0,
                                     period_entry.category))

    payments_command = ("INSERT INTO Payments(PeriodID, PayDate, Net)"
                        "VALUES(?, ?, ?)")
    payments = period_entry.payments
    items = []

    for i in payments:
        items.append((cursor.lastrowid, i.date, i.net))

    cursor.executemany(payments_command, items)
    connection.commit()


def get_period_entries() -> list[PeriodEntry]:
    periods = []
    cursor.execute("SELECT * FROM Periods")
    period_entries = cursor.fetchall()

    cursor.execute("SELECT * FROM Payments")
    all_payments = cursor.fetchall()
    payments_dict = {}

    for i in all_payments:
        payment = Payment(string_to_date(i[2]), i[3])
        if payments_dict.get(i[1], None) is None:
            payments_dict[i[1]] = [payment]
        else:
            payments_dict[i[1]].append(payment)

    for i in period_entries:
        payments = []
        if payments_dict.get(i[0], None) is not None:
            payments = payments_dict[i[0]]
        period = PeriodEntry(string_to_date(i[2]), string_to_date(i[3]), payments, i[7])
        periods.append(period)

    return periods
