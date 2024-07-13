import database
from report_generator import *


# entries = [
#     PeriodEntry(date(2024, 1, 1), date(2024, 2, 1),
#                 [Payment(date(2024, 1, 1), 1000),
#                  Payment(date(2024, 1, 15), 1000)],
#                 "Any"),
#     PeriodEntry(date(2024, 1, 1), date(2024, 3, 1),
#                 [Payment(date(2024, 3, 1), 500),
#                  Payment(date(2024, 3, 15), 500)],
#                 "Any"),
#     PeriodEntry(date(2024, 1, 1), date(2024, 4, 1),
#                 [Payment(date(2024, 4, 1), 500),
#                  Payment(date(2024, 4, 15), 500)],
#                 "Any")
# ]


entries = database.get_period_entries()
my_report = generate_report(period_entries=entries,
                            report_start=date(2024, 1, 1),
                            report_end=date(2024, 5, 31))
display_report(my_report)
