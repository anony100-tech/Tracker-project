import csv
import math
import os
from datetime import datetime

FILENAME = "expenses.csv"
FIELDS = ["date", "type", "category", "amount", "description"]


def save_entries(entries):
    with open(FILENAME, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for e in entries:
            row = dict(e)
            row["amount"] = f"{e['amount']:.2f}"
            writer.writerow(row)


def load_entries():
    entries = []
    if not os.path.exists(FILENAME):
        save_entries(entries)
        return entries
    with open(FILENAME, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            row["amount"] = float(row["amount"])
            entries.append(row)
    return entries


def get_amount():
    raw = input("Amount (NGN): ").strip().replace(",", "")
    try:
        amount = float(raw)
    except ValueError:
        print("Error: amount must be a positive number.")
        return None
    if not math.isfinite(amount) or amount <= 0:
        print("Error: amount must be a positive number.")
        return None
    return round(amount, 2)


def get_date():
    raw = input("Date (YYYY-MM-DD): ").strip()
    try:
        datetime.strptime(raw, "%Y-%m-%d")
    except ValueError:
        print("Error: date must look like 2026-06-15.")
        return None
    return raw

def balance(entries):
       income = sum(e["amount"] for e in entries if e["type"] == "income")
       spent = sum(e["amount"] for e in entries if e["type"] == "expense")
       return income - spent


def add_entry(entries, entry_type):
    date = get_date()
    if date is None:
        return

    if entry_type == "expense":
        category = input("Category (transport/food/data/rent/other): ")
    else:
        category = input("Category (e.g. salary): ")
    category = category.strip().lower() or "other"

    amount = get_amount()
    if amount is None:
        return

    description = input("Description: ").strip()

    entries.append({
        "date": date,
        "type": entry_type,
        "category": category,
        "amount": amount,
        "description": description,
    })
    save_entries(entries)
    print(f"{entry_type.capitalize()} saved. "
          f"Current balance: NGN {balance(entries):,.2f}")




def view_balance(entries):
    print(f"Current balance: NGN {balance(entries):,.2f}")


def summary(entries):
    totals = {}
    for e in entries:
        if e["type"] == "expense":
            cat = e["category"]
            totals[cat] = totals.get(cat, 0) + e["amount"]

    print("--- Summary by Category ---")
    if not totals:
        print("No expenses yet.")
    for cat, total in totals.items():
        print(f"{cat}: NGN {total:,.2f}")
    print("----------------------------")

def main():
    entries = load_entries()
    print("=== Personal Expense Tracker ===")
    while True:
        print("1. Add expense  2. Add income  3. View balance  "
              "4. Summary by category  5. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_entry(entries, "expense")
        elif choice == "2":
            add_entry(entries, "income")
        elif choice == "3":
            view_balance(entries)
        elif choice == "4":
            summary(entries)
        elif choice == "5":
            save_entries(entries)
            print("Goodbye! Data saved to expenses.csv")
            break
        else:
            print("Invalid option. Please choose 1 to 5.")
        print()


if __name__ == "__main__":
    main()
    