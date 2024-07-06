# from datetime import date
from datatypes import *
import database


def singular_report(period_entry: PeriodEntry, report_start: date, report_end: date) -> SimplifiedReport:
    work_start = period_entry.work_start
    work_end = period_entry.work_end

    work_period = (work_end - work_start).days
    payments = period_entry.payments
    period_value = sum(i.net for i in payments)

    current_profit_period = (min(work_end, report_end) - max(work_start, report_start)).days

    # in most cases profit_period shouldn't ever be lower than 0.
    if current_profit_period < 0:
        current_profit = 0
        print("Uh oh. current_profit_period less than 0. Double check inputs")
    elif work_period == 0:
        current_profit = period_value
    else:
        current_profit = round(period_value * (current_profit_period / work_period))

    total_reported_profit_period = round(((min(report_end, work_end)) - max(report_start, work_start)).days)
    total_reported_profit = round(period_value * (total_reported_profit_period / work_period), 2)

    prior_period_days = (report_start - work_start).days
    if prior_period_days < 0:
        prior_period_profit = 0
    else:
        prior_period_days = min(prior_period_days, work_period)
        prior_period_value = 0
        for i in payments:
            if i.date >= report_start:
                continue
            prior_period_value += i.net
        prior_period_profit = round(prior_period_value * (prior_period_days / work_period), 2)

    cash_flow = 0
    payments_made = 0  # this would include vat
    net_payments_made = 0  # this would not include vat
    for i in payments:
        payment_date = i.date
        if report_end >= payment_date >= report_start:
            cash_flow += i.net
        if report_end > payment_date:
            payments_made += i.net
            net_payments_made += i.net

    supplier_advances = int(max(total_reported_profit - net_payments_made, 0))

    report = SimplifiedReport(cash_flow, current_profit, payments_made, payments_made, supplier_advances,
                              current_profit, prior_period_profit)
    return report


def merge_reports(report_a: SimplifiedReport, report_b: SimplifiedReport) -> SimplifiedReport:
    cash_flow = report_a.cash_flow + report_b.cash_flow
    expense = report_a.expense + report_b.expense
    payments_sent = report_a.payments_sent + report_b.payments_sent
    amount_payable = report_a.amount_payable + report_b.amount_payable
    supplier_advances = report_a.supplier_advances + report_b.supplier_advances
    loss_in_period = report_a.loss_in_period + report_b.loss_in_period
    prior_loss_in_period = report_a.loss_in_period + report_b.loss_in_period

    new_report = SimplifiedReport(cash_flow,
                                  expense,
                                  payments_sent,
                                  amount_payable,
                                  supplier_advances,
                                  loss_in_period,
                                  prior_loss_in_period)

    return new_report


def generate_report(period_entries: list[PeriodEntry], report_start: date, report_end: date) -> SimplifiedReport:
    reports = []
    for i in period_entries:
        reports.append(singular_report(i, report_start, report_end))

    big_report = reports[0]
    for i in range(1, len(reports)):
        print(i)
        big_report = merge_reports(big_report, reports[i])

    return big_report


def display_report(report: SimplifiedReport):
    print("")
    print("********************* CUSTOMER FINANCIAL STATEMENT *************************")
    print("------------------------------CASH FLOW-------------------------------------")
    print("Cash outflow: ", report.cash_flow)
    print("-------------------------FINANCIAL PERFORMANCE------------------------------")
    print("Expense: ", report.expense)
    print("---------------------------FINANCIAL STANDING-------------------------------")
    print("Payments sent: ", report.payments_sent)
    print("Amount payable:", report.amount_payable)
    print("Supplier advances:", report.supplier_advances)
    print("Loss in report period: ", report.loss_in_period)
    print("Loss prior to report period:", report.prior_loss_in_period)
    print("")
    print("********************* SUPPLIER FINANCIAL STATEMENT *************************")
    print("------------------------------CASH FLOW-------------------------------------")
    print("Cash inflow: ", report.cash_flow)
    print("-------------------------FINANCIAL PERFORMANCE------------------------------")
    print("Income: ", report.expense)
    print("---------------------------FINANCIAL STANDING-------------------------------")
    print("Payments received: ", report.payments_sent)
    print("Amounts receivable:", report.amount_payable)
    print("Customer advances:", report.supplier_advances)
    print("Profit in report period: ", report.loss_in_period)
    print("Profit prior to report period:", report.prior_loss_in_period)


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

if __name__ == "__main__":
    entries = database.get_period_entries()
    my_report = generate_report(period_entries=entries,
                                report_start=date(2024, 1, 1),
                                report_end=date(2024, 5, 31))
    display_report(my_report)

    # for i in entries:
    #     database.add_period_entry(i)
