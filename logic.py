from collections import defaultdict
from datetime import datetime

def add_record(records, r_type, amount, category, note):
    record = {
        "type": r_type,
        "amount": amount,
        "category": category,
        "note": note,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    records.append(record)
    return records

def total_income_expense(records):
    income = sum(r["amount"] for r in records if r["type"] == "Income")
    expense = sum(r["amount"] for r in records if r["type"] == "Expense")
    return income, expense

def monthly_summary(records):
    summary = defaultdict(lambda: {"Income": 0, "Expense": 0})
    for r in records:
        date = datetime.strptime(r["timestamp"], "%Y-%m-%d %H:%M:%S")
        key = f"{date.year}-{date.month:02d}"
        summary[key][r["type"]] += r["amount"]
    return dict(summary)

def yearly_summary(records):
    summary = defaultdict(lambda: {"Income": 0, "Expense": 0})
    for r in records:
        date = datetime.strptime(r["timestamp"], "%Y-%m-%d %H:%M:%S")
        key = f"{date.year}"
        summary[key][r["type"]] += r["amount"]
    return dict(summary)

def check_budget(records, budget_limit):
    # Simple budget alert: returns True if expense exceeds budget
    _, expense = total_income_expense(records)
    return expense > budget_limit
