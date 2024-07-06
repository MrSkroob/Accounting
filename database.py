import sqlite3
import datetime
from datatypes import *


connection = sqlite3.connect("PE.db")
cursor = connection.cursor()


def add_period_entry(period_entry: PeriodEntry):
    periods_command = ("INSERT INTO periods(date_created, start_date, end_date, category, forecast_rule, calculation,"
                       " is_forecast)")

    cursor.execute(periods_command, (datetime.date.today(),
                                     period_entry.work_start,
                                     period_entry.work_end,
                                     period_entry.category,
                                     0,
                                     0,
                                     period_entry.category))

    payments_command = "INSERT INTO payments(PeriodID, date_created, net)"
    payments = period_entry.payments
    items = []

    for i in payments:
        items.append((cursor.lastrowid, i.date, i.net))

    cursor.executemany(payments_command, items)
    connection.commit()
