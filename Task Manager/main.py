# main.py
import tkinter as tk
from db import TaskDB
from task_gui import TaskManagerGUI
import datetime

def run_gui():
    root = tk.Tk()
    app = TaskManagerGUI(root)
    root.mainloop()

def run_cli():
    db = TaskDB()
    while True:
        print("\n" + "="*40)
        print("📝 AI Task Manager - CLI Mode")
        print("="*40)
        print("1. Add Task")
        print("2. List Tasks")
        print("3. Update Task Status")
        print("4. Edit Task")
        print("5. Delete Task")
        print("6. Search Task")
        print("7. Exit")
        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            title = input("Enter task title: ")
            priority = input("Priority (Low/Medium/High): ")
            due_date = input("Due date (YYYY-MM-DD): ")
            db.add_task(title, priority, due_date)
            print("✅ Task added!")

        elif choice == "2":
            tasks = db.list_tasks()
            if not tasks:
                print("No tasks found.")
            for t in tasks:
                print(f"[{t[0]}] {t[1]} | {t[2]} | {t[3]} | {t[4]}")

        elif choice == "3":
            task_id = int(input("Enter task ID to update status: "))
            current_status = input("Enter new status (Pending/Completed): ")
            db.update_task_status(task_id, current_status)
            print("✅ Task status updated!")

        elif choice == "4":
            task_id = int(input("Enter task ID to edit: "))
            title = input("New title (leave blank to skip): ").strip()
            priority = input("New priority (Low/Medium/High, leave blank to skip): ").strip()
            due_date = input("New due date (YYYY-MM-DD, leave blank to skip): ").strip()
            db.edit_task(task_id, title or None, priority or None, due_date or None)
            print("✅ Task updated!")

        elif choice == "5":
            task_id = int(input("Enter task ID to delete: "))
            db.delete_task(task_id)
            print("✅ Task deleted!")

        elif choice == "6":
            keyword = input("Enter keyword to search: ").strip().lower()
            tasks = [t for t in db.list_tasks() if keyword in t[1].lower()]
            if not tasks:
                print("No tasks found for this keyword.")
            for t in tasks:
                print(f"[{t[0]}] {t[1]} | {t[2]} | {t[3]} | {t[4]}")

        elif choice == "7":
            print("👋 Exiting CLI Task Manager. Goodbye!")
            db.close()
            break

        else:
            print("❌ Invalid choice, try again.")

if __name__ == "__main__":
    print("Select mode:")
    print("1. GUI Mode")
    print("2. CLI Mode")
    mode = input("Enter choice (1/2): ").strip()
    if mode == "1":
        run_gui()
    else:
        run_cli()
