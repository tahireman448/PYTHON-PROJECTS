import json
import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk

DATA_FILE = "expenses.json"

def load_expenses():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []

def save_expenses(expenses):
    with open(DATA_FILE, "w") as file:
        json.dump(expenses, file, indent=4)

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Daily Expense Tracker")
        self.root.geometry("650x450")
        self.root.config(bg="#f4f4f9")

        self.expenses = load_expenses()

        # Title Label
        title_label = tk.Label(root, text="Daily Expense Tracker", font=("Arial", 18, "bold"), bg="#f4f4f9", fg="#333")
        title_label.pack(pady=10)

        # Input Frame
        input_frame = tk.Frame(root, bg="#f4f4f9")
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Category:", font=("Arial", 10), bg="#f4f4f9").grid(row=0, column=0, padx=5, sticky="w")
        self.category_entry = tk.Entry(input_frame, font=("Arial", 10), width=15)
        self.category_entry.grid(row=0, column=1, padx=5)

        tk.Label(input_frame, text="Amount:", font=("Arial", 10), bg="#f4f4f9").grid(row=0, column=2, padx=5, sticky="w")
        self.amount_entry = tk.Entry(input_frame, font=("Arial", 10), width=12)
        self.amount_entry.grid(row=0, column=3, padx=5)

        tk.Label(input_frame, text="Description:", font=("Arial", 10), bg="#f4f4f9").grid(row=0, column=4, padx=5, sticky="w")
        self.desc_entry = tk.Entry(input_frame, font=("Arial", 10), width=18)
        self.desc_entry.grid(row=0, column=5, padx=5)

        # Add Button
        add_btn = tk.Button(root, text="Add Expense", font=("Arial", 10, "bold"), bg="#4CAF50", fg="white", command=self.add_expense)
        add_btn.pack(pady=5)

        # Treeview Table for Displaying Expenses
        table_frame = tk.Frame(root)
        table_frame.pack(pady=10)

        self.tree = ttk.Treeview(table_frame, columns=("Date", "Category", "Amount", "Description"), show="headings", height=8)
        self.tree.heading("Date", text="Date & Time")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Description", text="Description")

        self.tree.column("Date", width=140)
        self.tree.column("Category", width=110)
        self.tree.column("Amount", width=90)
        self.tree.column("Description", width=230)
        self.tree.pack()

        # Total Spending Label
        self.total_label = tk.Label(root, text="", font=("Arial", 12, "bold"), bg="#f4f4f9", fg="#d9534f")
        self.total_label.pack(pady=10)

        self.refresh_table()

    def add_expense(self):
        category = self.category_entry.get().strip().capitalize()
        amount_str = self.amount_entry.get().strip()
        description = self.desc_entry.get().strip()

        if not category or not amount_str:
            messagebox.showerror("Error", "Category and Amount fields cannot be blank!")
            return

        try:
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid positive number for the amount!")
            return

        expense = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "category": category,
            "amount": amount,
            "description": description if description else "N/A"
        }

        self.expenses.append(expense)
        save_expenses(self.expenses)
        self.refresh_table()

        # Clear inputs
        self.category_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        messagebox.showinfo("Success", "Expense added successfully!")

    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        total = 0
        for exp in self.expenses:
            self.tree.insert("", tk.END, values=(exp["date"], exp["category"], f"{exp['amount']:.2f}", exp["description"]))
            total += exp["amount"]

        self.total_label.config(text=f"Total Spending: {total:.2f}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()
