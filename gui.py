import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

def load_records():
    if not os.path.exists("records.json"):
        return []
    with open("records.json", "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_records(records):
    with open("records.json", "w") as f:
        json.dump(records, f, indent=4)

class BudgetApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("BudgetBuddy - Simple Finance Tool")
        self.geometry("650x550")
        self.resizable(False, False)
        self.records = load_records()
        self.create_widgets()
        self.refresh_records()

    def create_widgets(self):
        entry_frame = ttk.Frame(self)
        entry_frame.pack(pady=10, padx=10, fill="x")

        ttk.Label(entry_frame, text="Date (YYYY-MM-DD):").grid(row=0, column=0, sticky="w", padx=5)
        self.date_entry = ttk.Entry(entry_frame, width=12)
        self.date_entry.grid(row=0, column=1, padx=5)

        ttk.Label(entry_frame, text="Category:").grid(row=0, column=2, sticky="w", padx=5)
        self.category_entry = ttk.Entry(entry_frame, width=12)
        self.category_entry.grid(row=0, column=3, padx=5)

        ttk.Label(entry_frame, text="Amount:").grid(row=0, column=4, sticky="w", padx=5)
        self.amount_entry = ttk.Entry(entry_frame, width=8)
        self.amount_entry.grid(row=0, column=5, padx=5)

        ttk.Label(entry_frame, text="Note:").grid(row=1, column=0, sticky="w", padx=5)
        self.note_entry = ttk.Entry(entry_frame, width=52)
        self.note_entry.grid(row=1, column=1, columnspan=5, padx=5, pady=5, sticky="w")

        add_button = ttk.Button(entry_frame, text="Add Record", command=self.add_record)
        add_button.grid(row=2, column=0, columnspan=6, pady=5, sticky="ew")

        query_frame = ttk.Frame(self)
        query_frame.pack(pady=10, padx=10, fill='x')

        ttk.Label(query_frame, text="Year (e.g. 2025):").grid(row=0, column=0, sticky='w', padx=5)
        self.year_entry = ttk.Entry(query_frame, width=8)
        self.year_entry.grid(row=0, column=1, sticky='w', padx=5)

        ttk.Label(query_frame, text="Month (1-12, optional):").grid(row=0, column=2, sticky='w', padx=5)
        self.month_entry = ttk.Entry(query_frame, width=5)
        self.month_entry.grid(row=0, column=3, sticky='w', padx=5)

        query_button = ttk.Button(query_frame, text="Query Income", command=self.query_income)
        query_button.grid(row=0, column=4, sticky='w', padx=10)

        self.income_result_label = ttk.Label(self, text="", font=("Helvetica", 12, "bold"))
        self.income_result_label.pack(pady=5)

        tree_frame = ttk.Frame(self)
        tree_frame.pack(pady=10, padx=10, fill='both', expand=True)

        columns = ("date", "category", "amount", "note")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
        self.tree.heading("date", text="Date")
        self.tree.heading("category", text="Category")
        self.tree.heading("amount", text="Amount")
        self.tree.heading("note", text="Note")
        self.tree.column("date", width=100)
        self.tree.column("category", width=100)
        self.tree.column("amount", width=80)
        self.tree.column("note", width=250)
        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        del_button = ttk.Button(self, text="Delete Selected", command=self.delete_record)
        del_button.pack(pady=5)

    def add_record(self):
        date_str = self.date_entry.get().strip()
        category = self.category_entry.get().strip()
        amount_str = self.amount_entry.get().strip()
        note = self.note_entry.get().strip()

        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Invalid Date", "Please enter date in YYYY-MM-DD format.")
            return

        try:
            amount = float(amount_str)
        except ValueError:
            messagebox.showerror("Invalid Amount", "Please enter a valid number for amount.")
            return

        if not category:
            messagebox.showerror("Missing Category", "Please enter a category.")
            return

        record = {
            "date": date_str,
            "category": category,
            "amount": amount,
            "note": note
        }

        self.records.append(record)
        save_records(self.records)
        self.refresh_records()

        self.date_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.note_entry.delete(0, tk.END)

    def refresh_records(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for r in self.records:
            date = r.get("date", "N/A")
            category = r.get("category", "N/A")
            amount = r.get("amount", 0.0)
            note = r.get("note", "")
            self.tree.insert("", "end", values=(date, category, f"${amount:.2f}", note))

    def delete_record(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a record to delete.")
            return
        index = self.tree.index(selected_item)
        del self.records[index]
        save_records(self.records)
        self.refresh_records()

    def query_income(self):
        year_text = self.year_entry.get().strip()
        month_text = self.month_entry.get().strip()

        if not year_text.isdigit():
            messagebox.showerror("Input Error", "Please enter a valid year (numbers only).")
            return
        year = int(year_text)

        month = None
        if month_text:
            if not month_text.isdigit():
                messagebox.showerror("Input Error", "Month must be a number between 1 and 12 or empty.")
                return
            month = int(month_text)
            if month < 1 or month > 12:
                messagebox.showerror("Input Error", "Month must be between 1 and 12.")
                return

        total_income = 0.0
        for r in self.records:
            try:
                date_obj = datetime.strptime(r.get("date", ""), "%Y-%m-%d")
            except Exception:
                continue
            amount = r.get("amount", 0)
            if amount <= 0:
                continue
            if date_obj.year == year:
                if month is None or date_obj.month == month:
                    total_income += amount

        if month:
            result_text = f"Total income for {year}-{month:02d}: ${total_income:.2f}"
        else:
            result_text = f"Total income for year {year}: ${total_income:.2f}"

        self.income_result_label.config(text=result_text)

if __name__ == "__main__":
    app = BudgetApp()
    app.mainloop()
