# db.py
import sqlite3
import datetime
from typing import List, Tuple, Optional

DB_PATH = "tasks.db"

class TaskDB:
    def __init__(self, db_path=DB_PATH):
        self.conn = sqlite3.connect(db_path)
        self._create_table()

    def _create_table(self):
        cur = self.conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            priority TEXT,
            due_date TEXT,
            status TEXT,
            created_at TEXT NOT NULL DEFAULT (datetime('now','localtime'))
        )
        """)
        self.conn.commit()

    # ---------------- CRUD Operations ----------------
    def add_task(self, title: str, priority: str, due_date: str):
        cur = self.conn.cursor()
        created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cur.execute(
            "INSERT INTO tasks (title, priority, due_date, status, created_at) VALUES (?, ?, ?, ?, ?)",
            (title, priority, due_date, "Pending", created_at)
        )
        self.conn.commit()

    def list_tasks(self, status: Optional[str] = None, priority: Optional[str] = None) -> List[Tuple]:
        cur = self.conn.cursor()
        query = "SELECT id, title, priority, due_date, status FROM tasks"
        conditions = []
        params = []

        if status:
            conditions.append("status = ?")
            params.append(status)
        if priority:
            conditions.append("priority = ?")
            params.append(priority)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " ORDER BY id DESC"

        cur.execute(query, params)
        return cur.fetchall()  # Returns a list of tuples

    def update_task_status(self, task_id: int, status: str):
        cur = self.conn.cursor()
        cur.execute("UPDATE tasks SET status=? WHERE id=?", (status, task_id))
        self.conn.commit()

    def edit_task(self, task_id: int, title: Optional[str] = None, priority: Optional[str] = None, due_date: Optional[str] = None):
        cur = self.conn.cursor()
        updates = []
        params = []

        if title:
            updates.append("title = ?")
            params.append(title)
        if priority:
            updates.append("priority = ?")
            params.append(priority)
        if due_date:
            updates.append("due_date = ?")
            params.append(due_date)

        if updates:
            params.append(task_id)
            cur.execute(f"UPDATE tasks SET {', '.join(updates)} WHERE id = ?", params)
            self.conn.commit()

    def delete_task(self, task_id: int):
        cur = self.conn.cursor()
        cur.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        self.conn.commit()

    def search_tasks(self, keyword: str) -> List[Tuple]:
        cur = self.conn.cursor()
        like_kw = f"%{keyword}%"
        cur.execute("SELECT id, title, priority, due_date, status FROM tasks WHERE title LIKE ?", (like_kw,))
        return cur.fetchall()

    def close(self):
        self.conn.close()
