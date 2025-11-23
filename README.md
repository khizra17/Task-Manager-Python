A simple yet powerful Task Manager application built using Python, Tkinter, and SQLite, designed to help you organize tasks with clean visuals, sorting, filtering, and easy management.

This project includes a polished GUI with dark mode, priority-based color coding, CSV export, and automatic reminders for due and overdue tasks — perfect for students and professionals.

🚀 Features
✔ Task Management

Add new tasks

Edit existing tasks

Delete tasks

Mark tasks as Completed / Pending

Search tasks in real time

Sort by any column

Filter by:

Priority (Low, Medium, High)

Status (Pending, Completed)

🎨 Smart UI Enhancements

Priority-based color highlighting

Overdue and Due-Soon warnings (auto-highlighted)

Dark Mode 🌙

Popup reminders for:

Tasks due today

Overdue tasks

Clean and modern Tkinter interface

📁 Extras

Export tasks to CSV

Permanent storage using SQLite

Auto-created database (tasks.db)

📂 Project Structure
AI Task Manager/
│── Task Manager/
│   ├── main.py            # Starts the GUI
│   ├── task_gui.py        # Full Tkinter GUI code
│   ├── db.py              # SQLite database operations
│   ├── tasks.db           # Auto-created database
│   ├── screenshots/
│
│
└── README.md


Add your screenshots inside the screenshots/ folder.

🖼️ Screenshots
🏠 Main Window

➕ Add Task Popup

🌙 Dark Mode

🔧 Installation & Setup
1️⃣ Clone this Repository
git clone https://github.com/your-username/python-task-manager-gui.git
cd python-task-manager-gui

2️⃣ Run the Application
python main.py


No external packages required — Tkinter & SQLite are built into Python.

🧠 How It Works

Your data is stored in a local SQLite database (tasks.db).
Each task entry includes:

id

title

priority

due_date

status

The GUI interacts with this database through db.py, providing a smooth and instant update experience.

📤 Export to CSV

You can export all tasks into a CSV file using the Export CSV button.

Format:

ID	Title	Priority	Due Date	Status
🌟 Future Enhancements (Optional Ideas)

Categories / Labels

Task notifications

Recurring tasks

Enhanced themes (light/dark/blue)

Cloud sync

🤝 Contributing

Pull requests are welcome!
If you improve this project, feel free to contribute.

⭐ Support

If you like this project, don’t forget to ⭐ star the repository on GitHub!