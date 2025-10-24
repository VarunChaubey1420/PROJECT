# medicine_stock_checker/app.py
"""
Medicine Stock Checker - simple Tkinter app.
Run: python app.py
"""

import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os
from datetime import datetime

DATA_FILE = "medicines.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                return json.load(f)
            except:
                return []
    return []

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Medicine Stock Checker")
        self.data = load_data()

        # UI
        self.frame = tk.Frame(root, padx=10, pady=10)
        self.frame.pack()

        tk.Label(self.frame, text="Medicine Name").grid(row=0, column=0)
        tk.Label(self.frame, text="Qty").grid(row=0, column=1)
        tk.Label(self.frame, text="Expiry (YYYY-MM-DD)").grid(row=0, column=2)

        self.name_entry = tk.Entry(self.frame)
        self.qty_entry = tk.Entry(self.frame)
        self.exp_entry = tk.Entry(self.frame)

        self.name_entry.grid(row=1, column=0)
        self.qty_entry.grid(row=1, column=1)
        self.exp_entry.grid(row=1, column=2)

        tk.Button(self.frame, text="Add / Update", command=self.add_update).grid(row=1, column=3)
        tk.Button(self.frame, text="Delete", command=self.delete_item).grid(row=1, column=4)
        tk.Button(self.frame, text="Refresh", command=self.refresh_list).grid(row=1, column=5)

        self.listbox = tk.Listbox(root, width=80)
        self.listbox.pack(padx=10, pady=10)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)

        self.status = tk.Label(root, text="", anchor="w")
        self.status.pack(fill="x")

        self.refresh_list()
        self.check_expiry_on_start()

    def add_update(self):
        name = self.name_entry.get().strip()
        qty = self.qty_entry.get().strip()
        exp = self.exp_entry.get().strip()
        if not name or not qty:
            messagebox.showwarning("Input", "Please enter name and quantity.")
            return
        try:
            qty = int(qty)
        except:
            messagebox.showerror("Input", "Quantity must be an integer.")
            return
        # validate expiry
        if exp:
            try:
                datetime.strptime(exp, "%Y-%m-%d")
            except:
                messagebox.showerror("Input", "Expiry must be YYYY-MM-DD or empty.")
                return

        # update if exists
        found = False
        for item in self.data:
            if item["name"].lower() == name.lower():
                item["qty"] = qty
                item["expiry"] = exp
                found = True
                break
        if not found:
            self.data.append({"name": name, "qty": qty, "expiry": exp})
        save_data(self.data)
        self.refresh_list()
        self.status.config(text=f"Saved '{name}'")

    def delete_item(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showinfo("Delete", "Please select an item first.")
            return
        idx = sel[0]
        item = self.data.pop(idx)
        save_data(self.data)
        self.refresh_list()
        self.status.config(text=f"Deleted '{item['name']}'")

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for item in self.data:
            line = f"{item['name']} — Qty: {item['qty']}"
            if item.get("expiry"):
                line += f" — Expiry: {item['expiry']}"
            self.listbox.insert(tk.END, line)

    def on_select(self, event):
        sel = self.listbox.curselection()
        if not sel:
            return
        item = self.data[sel[0]]
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, item["name"])
        self.qty_entry.delete(0, tk.END)
        self.qty_entry.insert(0, item["qty"])
        self.exp_entry.delete(0, tk.END)
        self.exp_entry.insert(0, item.get("expiry", ""))

    def check_expiry_on_start(self):
        today = datetime.now().date()
        expired = []
        near_expiry = []
        for item in self.data:
            exp = item.get("expiry")
            if exp:
                try:
                    exp_date = datetime.strptime(exp, "%Y-%m-%d").date()
                    if exp_date < today:
                        expired.append(item["name"])
                    elif (exp_date - today).days <= 30:
                        near_expiry.append(item["name"])
                except:
                    pass
        msg = ""
        if expired:
            msg += "Expired: " + ", ".join(expired) + ". "
        if near_expiry:
            msg += "Near expiry (<=30 days): " + ", ".join(near_expiry) + "."
        if msg:
            messagebox.showinfo("Expiry Check", msg)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
