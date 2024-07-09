import init_database
import sqlite3
import csv


def to_int(data: str):
    if data == "":
        return 0
    elif data == "FALSE":
        return 0
    elif data == "TRUE":
        return 1
    else:
        return int(data)


def to_float(data: str):
    if data == "":
        return 0
    else:
        return float(data)


def string_to_type(data: str, data_type: str):
    match data_type:
        case "NULL":
            return None
        case "INTEGER":
            return to_int(data)
        case "NUMERIC":
            return to_float(data)
        case "REAL":
            return to_float(data)
        case "TEXT":
            return data
        case "BLOB":
            return data


def csv_to_db(csv_path: str, db_type: str):
    connection = sqlite3.connect("ConvertedCSVs/PE.db")
    cursor = connection.cursor()

    cursor.execute("DROP TABLE IF EXISTS " + db_type)

    if db_type == "Periods":
        header = init_database.PERIODS_HEADER
        column_types = init_database.PERIODS_TYPES
        cursor.execute(init_database.PERIODS_TABLE)
    elif db_type == "Payments":
        header = init_database.PAYMENTS_HEADER
        column_types = init_database.PAYMENTS_TYPES
        cursor.execute(init_database.PAYMENTS_TABLE)
    else:
        raise NotImplementedError("Not implemented " + db_type)

    header_string = ", ".join(header)
    values_string = "?, " * len(header)
    values_string = values_string.strip(", ")

    with open(csv_path, mode="r") as f:
        sql = "INSERT INTO " + db_type + " (" + header_string + ") VALUES (" + values_string + ")"
        reader = csv.reader(f)

        values = []
        index = 0
        for row in reader:
            index += 1
            if index == 1:
                continue
            data = []
            for i, item in enumerate(row):
                try:
                    data.append(string_to_type(item, column_types[i]))
                except IndexError:
                    print("WARNING: More columns received than expected, ignoring")
                    continue
            values.append(tuple(data))

        cursor.executemany(sql, values)

    connection.commit()


if __name__ == "__main__":
    csv_to_db("ImportedCSVs/Online training course - Period.csv", "Periods")
    csv_to_db("ImportedCSVs/Online training course - Payment.csv", "Payments")
