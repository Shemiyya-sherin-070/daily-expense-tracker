import csv
import os
import uuid
class Expense:
    def __init__(self, date, category, item, amount, _id=None):
        self.id = _id or str(uuid.uuid4())
        self.date = date
        self.category = category
        self.item = item
        self.amount = amount
    def to_list(self):
        return [
            self.date,
            self.category,
            self.item,
            self.amount
        ]
class ExpenseManager:
    def __init__(self, file_name="expenses.csv"):
        self.file_name = file_name
        self.expenses = []
        self.load_expenses()
    def load_expenses(self):
        self.expenses = []
        if not os.path.exists(self.file_name):
            return
        with open(self.file_name, "r", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    self.expenses.append({
                    "id": row["id"],
                    "date": row["date"],
                    "category": row["category"],
                    "item": row["item"],
                    "amount": row["amount"]
                    })
                except(ValueError,TypeError):
                    continue
    def save_expenses(self):
        with open(self.file_name, "w", newline="") as f:
            fieldnames = [
                "id",
                "date",
                "category",
                "item",
                "amount"
            ]
            writer = csv.DictWriter(
                f,
                fieldnames=fieldnames
            )
            writer.writeheader()
            for e in self.expenses:
                writer.writerow({
                    "id": e["id"],
                    "date": e["date"],
                    "category": e["category"],
                    "item": e["item"],
                    "amount": e["amount"]
                })
    def add_expense(self, expense):
        self.expenses.append({
            "id": expense.id,
            "date": expense.date,
            "category": expense.category,
            "item": expense.item,
            "amount": expense.amount
        })
        self.save_expenses()
    def delete_expense(self, expense_id):
        self.expenses = [
            e for e in self.expenses
            if e["id"] != expense_id
        ]
        self.save_expenses()
    def update_expense(self, expense_id, updated):
        for i, e in enumerate(self.expenses):
            if e["id"] == expense_id:
                self.expenses[i] = {
                    "id": expense_id,
                    "date": updated.date,
                    "category": updated.category,
                    "item": updated.item,
                    "amount": updated.amount
                }
                break
        self.save_expenses()
    def get_total(self):
        return sum(
            float(e.get("amount",0))
            for e in self.expenses
        )
    def get_expenses(self):
        return self.expenses