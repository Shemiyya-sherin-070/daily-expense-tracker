import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import datetime
from backend import Expense,ExpenseManager

class ExpenseTrackerApp:
    def __init__(self, root):
        self.manager = ExpenseManager()
        self.root = root
        self.root.title("Daily Expense Tracker")
        self.root.geometry("800x850")

        self.selected_id = None
        self.category_var = tk.StringVar()
        self.item_var = tk.StringVar()
        self.amount_var = tk.StringVar()

        self.create_widgets()
        self.load_table()

    def create_widgets(self):
        self.root.configure(bg="#f4f6f8")
        
        title = tk.Label(
            self.root,
            text="Daily Expense Tracker",
            font=("Helvetica", 24, "bold"),
            bg="#f4f6f8",
            fg="#2c3e50"
        )
        title.pack(pady=15)
        form = tk.Frame(
            self.root,
            bg="white",
            bd=2,
            relief="groove",
            padx=20,
            pady=20
        )
        form.pack(padx=20, pady=10)
        label_style = {
            "font": ("Arial", 11, "bold"),
            "bg": "white",
            "fg": "#333"
        }

        entry_style = {
            "font": ("Arial", 11),
            "width": 25
        }

        tk.Label(form, text="Date", **label_style).grid(row=0, column=0, sticky="w", padx=10, pady=8)
        self.cal=DateEntry(form,width=12,bg="darkblue",fg="white",borderwidth=2,date_pattern="dd-mm-yyyy",maxdate=datetime.date.today())
        self.cal.grid(row=0, column=1, padx=10, pady=8)
        self.cal.bind("<<DateEntrySelected>>", lambda e: self.load_table())
        tk.Button(self.root,text="Select date",command={self.cal.get_date()})

        tk.Label(form, text="Category", **label_style).grid(row=1, column=0, sticky="w", padx=10, pady=8)
        categories = [
            "Food",
            "Transport",
            "Rent",
            "Shopping",
            "Health",
            "Entertainment",
            "Other"
        ]

        self.category_combo = ttk.Combobox(
            form,
            textvariable=self.category_var,
            values=categories,
            state="readonly",
            width=23
        )

        self.category_combo.grid(row=1, column=1)
        self.category_combo.set("Select Category")
        tk.Label(form, text="Item", **label_style).grid(row=2, column=0, sticky="w", padx=10, pady=8)
        tk.Entry(form, textvariable=self.item_var, **entry_style).grid(row=2, column=1)

        tk.Label(form, text="Amount", **label_style).grid(row=3, column=0, sticky="w", padx=10, pady=8)
        tk.Entry(form, textvariable=self.amount_var, **entry_style).grid(row=3, column=1)

        button_frame = tk.Frame(form, bg="white")
        button_frame.grid(row=4, column=0, columnspan=2, pady=15)

        tk.Button(
            button_frame,
            text="Add",
            command=self.add_expense,
            bg="#27ae60",
            fg="white",
            font=("Arial", 11, "bold"),
            width=12,
            relief="flat",
            cursor="hand2"
        ).grid(row=0, column=0, padx=8)

        button_frame.grid_columnconfigure(0,weight=1)
        button_frame.grid_columnconfigure(1,weight=1)
        tk.Button(
            button_frame,
            text="Update",
            command=self.update_expense,
            bg="#2980b9",
            fg="white",
            font=("Arial", 11, "bold"),
            width=12,
            relief="flat",
            cursor="hand2"
        ).grid(row=0, column=1, padx=10)
        


        table_frame = tk.Frame(self.root, bg="#f4f6f8")
        table_frame.pack(padx=20, pady=10)

        columns=("Date", "Category", "Item", "Amount")
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=10
        )
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col,width=150)
        self.tree.pack()
        self.tree.bind("<ButtonRelease-1>", self.select_item)

        button_frame=tk.Frame(self.root,bg="#f4f6f8")
        button_frame.pack(pady=10)
                
        tk.Button(
            button_frame,
            text="Delete Selected",
            command=self.delete_expense,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 11, "bold"),
            width=18,
        ).grid(row=0, column=1, padx=10)

        self.total_label = tk.Label(
            self.root,
            text="Total: 0",
            font=("Arial", 14, "bold"),
            bg="#f4f6f8",
            fg="#2c3e50"
        )
        self.total_label.pack(pady=10)
    
    def validate_input(self):

        try:
            amount=float(self.amount_var.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Amount must be numeric")
            return False

        return True

    def add_expense(self):
        if not self.validate_input():
            return

        date_str = self.cal.get_date().strftime("%Y-%m-%d")
        exp = Expense(
            date_str,
            self.category_var.get(),
            self.item_var.get(),
            float(self.amount_var.get()),  
        )

        self.manager.add_expense(exp)
        self.load_table()
        self.clear_fields()

    def update_expense(self):
        if not self.selected_id:
            messagebox.showerror("Error", "No item selected")
            return
        date_str = self.cal.get_date().strftime("%Y-%m-%d")
        exp = Expense(
            date_str,
            self.category_var.get(),
            self.item_var.get(),
            float(self.amount_var.get()),
            _id=self.selected_id
        )

        self.manager.update_expense(self.selected_id, exp)
        self.load_table()
        self.clear_fields()

    def delete_expense(self):
        if not self.selected_id:
            messagebox.showerror("Error", "Select an item first")
            return

        self.manager.delete_expense(self.selected_id)
        self.load_table()
        self.clear_fields()

    def load_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        selected_date = self.cal.get_date().strftime("%Y-%m-%d")
        current_date_total = 0

        for e in self.manager.expenses:
            if e["date"] == selected_date:
                self.tree.insert(
                    "",
                    tk.END,
                    iid=e["id"],
                    values=(e["date"], e["category"], e["item"], e["amount"])
                )
                current_date_total += float(e["amount"])
        self.total_label.config(text=f"Total for {selected_date}: {current_date_total}")

    def select_item(self, event):
        selected = self.tree.focus()
        if selected:
            values = self.tree.item(selected, "values")
            self.selected_id = selected

            from datetime import datetime
            date_obj = datetime.strptime(values[0], "%Y-%m-%d")
            self.cal.set_date(date_obj)
            self.category_var.set(values[1])
            self.item_var.set(values[2])
            self.amount_var.set(values[3])
    
    def clear_fields(self):
        import datetime
        self.cal.set_date(datetime.date.today())
        self.category_combo.set("Select category")
        self.item_var.set("")
        self.amount_var.set("")
        self.selected_id = None

