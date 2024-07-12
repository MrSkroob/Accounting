import sqlite3
import datetime
import Utils.init_database as init_database
from datatypes import *


connection = sqlite3.connect("PE.db")
cursor = connection.cursor()


def _string_to_date(date_str: str) -> date:
    return datetime.datetime.strptime(date_str, "%d/%m/%Y").date()


def _date_to_string(date_: date) -> str:
    return date_.strftime("%d/%m/%Y")


def _key_to_index(dictionary: dict, key: any):
    return list(dictionary.keys()).index(key)


def add_period_entry(period_entry: PeriodEntry):
    columns = ", ".join(init_database.PERIODS_TYPES)

    periods_command = ("INSERT INTO Periods(" + columns + ")"
                       "VALUES(?, ?, ?, ?, ?, ?, ?)")

    input_list: list[any] = [None] * 5

    date_created_index = _key_to_index(init_database.PERIODS_TYPES, "DateCreated")
    work_start_index = _key_to_index(init_database.PERIODS_TYPES, "StartDate")
    work_end_index = _key_to_index(init_database.PERIODS_TYPES, "EndDate")
    category_index = _key_to_index(init_database.PERIODS_TYPES, "Category")
    forecast_rule_index = _key_to_index(init_database.PERIODS_TYPES, "ForecastRule")
    calculation_index = _key_to_index(init_database.PERIODS_TYPES, "Calculation")
    is_forecast_index = _key_to_index(init_database.PERIODS_TYPES, "IsForecast")

    input_list[date_created_index] = datetime.date.today().strftime("%d/%m/%Y")
    input_list[work_start_index] = period_entry.work_start
    input_list[work_end_index] = period_entry.work_end
    input_list[category_index] = period_entry.category
    input_list[forecast_rule_index] = 0
    input_list[calculation_index] = 0
    input_list[is_forecast_index] = period_entry.is_forecast

    cursor.execute(periods_command, input_list)

    payments_command = ("INSERT INTO Payments(PeriodID, PayDate, Net)"
                        "VALUES(?, ?, ?)")
    payments = period_entry.payments
    items = []

    for i in payments:
        items.append((cursor.lastrowid, i.date, i.net))

    cursor.executemany(payments_command, items)
    connection.commit()


def get_period_entries(start_date: date = None, end_date: date = None) -> list[PeriodEntry]:
    periods = []
    periods_sql = "SELECT * FROM Periods"
    if start_date is not None and end_date is not None:
        periods_sql += ("  WHERE StartDate < " +
                        _date_to_string(end_date) +
                        " AND StartDate" > _date_to_string(start_date))

    cursor.execute(periods_sql)
    period_entries = cursor.fetchall()

    cursor.execute("SELECT * FROM Payments")
    all_payments = cursor.fetchall()
    payments_dict = {}

    period_id_index = _key_to_index(init_database.PAYMENTS_TYPES, "PeriodID")
    date_index = _key_to_index(init_database.PAYMENTS_TYPES, "PayDate")
    net_index = _key_to_index(init_database.PAYMENTS_TYPES, "Net")

    for i in all_payments:
        payment = Payment(_string_to_date(i[date_index]), i[net_index])
        if payments_dict.get(i[period_id_index], None) is None:
            payments_dict[i[period_id_index]] = [payment]
        else:
            payments_dict[i[period_id_index]].append(payment)

    period_id_index = _key_to_index(init_database.PERIODS_TYPES, "PeriodID")
    work_start_index = _key_to_index(init_database.PERIODS_TYPES, "StartDate")
    work_end_index = _key_to_index(init_database.PERIODS_TYPES, "EndDate")
    category_index = _key_to_index(init_database.PERIODS_TYPES, "Category")
    is_forecast_index = _key_to_index(init_database.PERIODS_TYPES, "IsForecast")

    for i in period_entries:
        payments = []
        if payments_dict.get(i[period_id_index], None) is not None:
            payments = payments_dict[i[period_id_index]]
        period = PeriodEntry(_string_to_date(i[work_start_index]),
                             _string_to_date(i[work_end_index]),
                             payments,
                             i[category_index],
                             i[is_forecast_index])
        periods.append(period)

    return periods
