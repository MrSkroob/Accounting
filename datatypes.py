from datetime import date
from dataclasses import dataclass


@dataclass
class Payment:
    date: date
    net: int  # in pence
    # vat: int


@dataclass
class PeriodEntry:
    work_start: date
    work_end: date
    payments: list[Payment]
    category: str
    is_forecast: bool
    # forecast_rule: str


@dataclass
class SimplifiedReport:
    cash_flow: int
    expense: int
    payments_sent: int
    amount_owed_and_owing: int
    loss_in_period: int
    prior_loss_in_period: int


@dataclass
class Report:
    report_start: date
    report_end: date

    centres: int = 0  # think 'course'
    clients: int = 0  # think 'student'

    income: int = 0
    gross_profit: int = 0
    gross_profit_percent: float = 0

    overhead: int = 0
    operating_profit: int = 0
    net_profit: int = 0
    net_profit_percent: int = 0
    corporate_tax: int = 0

    cash_flow: int = 0

    # these should sum to 0
    bank_balance: int = 0
    amount_due: int = 0
    amount_owing: int = 0
    current_profit: int = 0
    prior_period_profit: int = 0
