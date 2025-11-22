# task_gui.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from db import TaskDB
import datetime
import csv

class TaskManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("📋 Python Task Manager")
        self.root.geometry("800x550")
        self.db = TaskDB()
        self.dark_mode = False

        # ----------------- Header -----------------
        header = ttk.Label(root, text="📋 Python Task Manager", font=("Segoe UI", 16, "bold"))
        header.pack(pady=10)

        # ----------------- Top Frame -----------------
        self.top_frame = ttk.Frame(root, padding=10)
        self.top_frame.pack(fill="x")

        ttk.Label(self.top_frame, text="Task Title:").grid(row=0, column=0, sticky="w")
        self.title_entry = ttk.Entry(self.top_frame, width=30)
        self.title_entry.grid(row=0, column=1, padx=5)

        ttk.Label(self.top_frame, text="Priority:").grid(row=0, column=2, sticky="w")
        self.priority_cb = ttk.Combobox(self.top_frame, values=["Low", "Medium", "High"], state="readonly", width=10)
        self.priority_cb.current(1)
        self.priority_cb.grid(row=0, column=3, padx=5)

        ttk.Label(self.top_frame, text="Due Date (YYYY-MM-DD):").grid(row=1, column=0, sticky="w", pady=5)
        self.due_entry = ttk.Entry(self.top_frame, width=15)
        self.due_entry.grid(row=1, column=1, padx=5, pady=5)

        # Add task from fields directly
        self.add_button = ttk.Button(self.top_frame, text="➕ Add Task", command=self.add_task_from_fields)
        self.add_button.grid(row=1, column=3, padx=5, pady=5)

        # Optional: popup add button (if needed)
        self.popup_add_button = ttk.Button(self.top_frame, text="📝 Add via Popup", command=self.add_task_popup)
        self.popup_add_button.grid(row=1, column=4, padx=5, pady=5)

        # Search box
        ttk.Label(self.top_frame, text="🔍 Search:").grid(row=2, column=0, sticky="w", pady=5)
        self.search_entry = ttk.Entry(self.top_frame, width=30)
        self.search_entry.grid(row=2, column=1, padx=5, pady=5)
        self.search_entry.bind("<KeyRelease>", lambda e: self.refresh_tasks())

        # ----------------- Treeview -----------------
        columns = ("ID","Title","Priority","Due","Status")
        self.tree = ttk.Treeview(root, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_column(c, False))
        self.tree.pack(fill="both", expand=True, pady=10)

        # ----------------- Action Buttons -----------------
        action_frame = ttk.Frame(root)
        action_frame.pack(fill="x", pady=6)

        self.complete_button = ttk.Button(action_frame, text="✅ Toggle Complete", command=self.mark_complete)
        self.complete_button.pack(side="left", padx=4)

        self.edit_button = ttk.Button(action_frame, text="✏️ Edit Task", command=self.edit_task_popup)
        self.edit_button.pack(side="left", padx=4)

        self.delete_button = ttk.Button(action_frame, text="🗑 Delete Task", command=self.delete_task)
        self.delete_button.pack(side="left", padx=4)

        self.export_button = ttk.Button(action_frame, text="📁 Export CSV", command=self.export_csv)
        self.export_button.pack(side="left", padx=4)

        self.dark_button = ttk.Button(action_frame, text="🌙 Dark Mode", command=self.toggle_dark_mode)
        self.dark_button.pack(side="right", padx=4)

        self.filter_status = ttk.Combobox(action_frame, values=["All", "Pending", "Completed"], state="readonly", width=10)
        self.filter_status.current(0)
        self.filter_status.pack(side="right", padx=4)
        self.filter_status.bind("<<ComboboxSelected>>", lambda e: self.refresh_tasks())

        self.filter_priority = ttk.Combobox(action_frame, values=["All", "Low", "Medium", "High"], state="readonly", width=10)
        self.filter_priority.current(0)
        self.filter_priority.pack(side="right", padx=4)
        self.filter_priority.bind("<<ComboboxSelected>>", lambda e: self.refresh_tasks())

        # ----------------- Final Initialization -----------------
        self.refresh_tasks()
        self.show_due_reminders()

    # ----------------- Add Task from Top Fields -----------------
    def add_task_from_fields(self):
        title = self.title_entry.get().strip()
        priority = self.priority_cb.get()
        due_date = self.due_entry.get().strip()

        if not title or not due_date:
            messagebox.showwarning("Required", "Title and Due Date are required")
            return
        try:
            datetime.datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Invalid date", "Enter date in YYYY-MM-DD format")
            return

        self.db.add_task(title, priority, due_date)
        self.refresh_tasks()

        # Clear fields after adding
        self.title_entry.delete(0, tk.END)
        self.due_entry.delete(0, tk.END)
        self.priority_cb.current(1)

    # ----------------- Add Task via Popup -----------------
    def add_task_popup(self):
        win = tk.Toplevel(self.root)
        win.title("Add New Task")
        win.geometry("300x220")

        ttk.Label(win, text="Title:").pack(anchor="w", padx=8, pady=(8,0))
        title_entry = ttk.Entry(win, width=30)
        title_entry.pack(padx=8, pady=4)

        ttk.Label(win, text="Priority:").pack(anchor="w", padx=8, pady=(8,0))
        priority_cb = ttk.Combobox(win, values=["Low","Medium","High"], state="readonly", width=27)
        priority_cb.current(1)
        priority_cb.pack(padx=8, pady=4)

        ttk.Label(win, text="Due Date (YYYY-MM-DD):").pack(anchor="w", padx=8, pady=(8,0))
        due_entry = ttk.Entry(win, width=30)
        due_entry.pack(padx=8, pady=4)

        def save():
            title = title_entry.get().strip()
            priority = priority_cb.get()
            due_date = due_entry.get().strip()
            if not title or not due_date:
                messagebox.showwarning("Required", "Title and Due Date are required")
                return
            try:
                datetime.datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Invalid date", "Enter date in YYYY-MM-DD format")
                return
            self.db.add_task(title, priority, due_date)
            self.refresh_tasks()
            win.destroy()

        ttk.Button(win, text="Add Task", command=save).pack(pady=10)

    # ----------------- Edit Task -----------------
    def edit_task_popup(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Select Task", "Select a task to edit")
            return
        task_id = self.tree.item(sel[0])["values"][0]
        task = next((t for t in self.db.list_tasks() if t[0]==task_id), None)
        if not task:
            messagebox.showerror("Error", "Task not found")
            return

        win = tk.Toplevel(self.root)
        win.title("Edit Task")
        win.geometry("300x220")

        ttk.Label(win, text="Title:").pack(anchor="w", padx=8, pady=(8,0))
        title_entry = ttk.Entry(win, width=30)
        title_entry.insert(0, task[1])
        title_entry.pack(padx=8, pady=4)

        ttk.Label(win, text="Priority:").pack(anchor="w", padx=8, pady=(8,0))
        priority_cb = ttk.Combobox(win, values=["Low","Medium","High"], state="readonly", width=27)
        priority_cb.set(task[2])
        priority_cb.pack(padx=8, pady=4)

        ttk.Label(win, text="Due Date (YYYY-MM-DD):").pack(anchor="w", padx=8, pady=(8,0))
        due_entry = ttk.Entry(win, width=30)
        due_entry.insert(0, task[3])
        due_entry.pack(padx=8, pady=4)

        def save():
            title = title_entry.get().strip()
            priority = priority_cb.get()
            due_date = due_entry.get().strip()
            if not title or not due_date:
                messagebox.showwarning("Required", "Title and Due Date are required")
                return
            try:
                datetime.datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Invalid date", "Enter date in YYYY-MM-DD format")
                return
            self.db.edit_task(task_id, title, priority, due_date)
            self.refresh_tasks()
            win.destroy()

        ttk.Button(win, text="Save Changes", command=save).pack(pady=10)

    # ----------------- Refresh Tasks -----------------
    def refresh_tasks(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        status_filter = self.filter_status.get()
        priority_filter = self.filter_priority.get()
        search_text = self.search_entry.get().strip().lower()

        status = None if status_filter == "All" else status_filter
        priority = None if priority_filter == "All" else priority_filter

        tasks = self.db.list_tasks(status=status, priority=priority)
        for t in tasks:
            if search_text and search_text not in t[1].lower():
                continue

            due_date_obj = datetime.datetime.strptime(t[3], "%Y-%m-%d")
            days_left = (due_date_obj - datetime.datetime.now()).days

            # Tag logic: combine overdue/due_soon and priority
            tags = []
            if days_left < 0:
                tags.append("overdue")
            elif days_left <= 3:
                tags.append("due_soon")
            if t[2] == "High":
                tags.append("high_priority")
            elif t[2] == "Medium":
                tags.append("medium_priority")
            elif t[2] == "Low":
                tags.append("low_priority")

            self.tree.insert("", "end", values=t, tags=tags)

        # Tag colors
        self.tree.tag_configure("overdue", background="#ff9999")
        self.tree.tag_configure("due_soon", background="#fff2cc")
        self.tree.tag_configure("high_priority", foreground="#b30000", font=("Segoe UI", 10, "bold"))
        self.tree.tag_configure("medium_priority", foreground="#b38600", font=("Segoe UI", 10))
        self.tree.tag_configure("low_priority", foreground="#006600", font=("Segoe UI", 10))

    # ----------------- Actions -----------------
    def mark_complete(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Select Task", "Select a task to toggle completion")
            return
        task_id = self.tree.item(sel[0])["values"][0]
        status = self.tree.item(sel[0])["values"][4]
        new_status = "Completed" if status != "Completed" else "Pending"
        self.db.update_task_status(task_id, new_status)
        self.refresh_tasks()

    def delete_task(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Select Task", "Select a task to delete")
            return
        task_id = self.tree.item(sel[0])["values"][0]
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this task?"):
            self.db.delete_task(task_id)
            self.refresh_tasks()

    def export_csv(self):
        file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files","*.csv")])
        if not file:
            return
        tasks = self.db.list_tasks()
        with open(file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["ID","Title","Priority","Due Date","Status"])
            writer.writerows(tasks)
        messagebox.showinfo("Exported", f"Tasks exported to {file}")

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        style = ttk.Style()
        if self.dark_mode:
            self.root.configure(bg="#2e2e2e")
            style.theme_use('clam')
            style.configure(".", background="#2e2e2e", foreground="white")
        else:
            self.root.configure(bg="SystemButtonFace")
            style.theme_use('default')
        self.refresh_tasks()

    # ----------------- Reminders -----------------
    def show_due_reminders(self):
        tasks = self.db.list_tasks()
        due_today = []
        overdue = []
        for t in tasks:
            due_date = datetime.datetime.strptime(t[3], "%Y-%m-%d")
            if due_date.date() == datetime.datetime.now().date():
                due_today.append(t[1])
            elif due_date < datetime.datetime.now():
                overdue.append(t[1])
        msg = ""
        if overdue:
            msg += "⚠️ Overdue tasks:\n" + "\n".join(overdue) + "\n\n"
        if due_today:
            msg += "📅 Tasks due today:\n" + "\n".join(due_today)
        if msg:
            messagebox.showinfo("Reminders", msg)

    # ----------------- Sorting -----------------
    def sort_column(self, col, reverse):
        data = [(self.tree.set(k, col), k) for k in self.tree.get_children('')]
        if col in ["ID"]:
            data.sort(key=lambda t: int(t[0]), reverse=reverse)
        elif col in ["Due"]:
            data.sort(key=lambda t: datetime.datetime.strptime(t[0], "%Y-%m-%d"), reverse=reverse)
        else:
            data.sort(reverse=reverse)
        for index, (val, k) in enumerate(data):
            self.tree.move(k, '', index)
        self.tree.heading(col, command=lambda: self.sort_column(col, not reverse))
