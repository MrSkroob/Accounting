import sqlite3
from datatypes import *
from report_generator import generate_report


database_connection = sqlite3.connect("PE.db")
cursor = database_connection.cursor()


def add_period_entry(period_entry: PeriodEntry):
    command = "INSERT INTO payments(date, net)"
    payments = period_entry.payments

    for i in payments:
        pass
