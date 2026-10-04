import os
import sqlite3
from datetime import datetime

from app.config import DB_PATH


def con():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_db():
    c = con()
    q = c.cursor()

    q.execute("""
        CREATE TABLE IF NOT EXISTS users(
            username TEXT PRIMARY KEY,
            password TEXT,
            role TEXT
        )
    """)

    q.execute("""
        CREATE TABLE IF NOT EXISTS predictions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT,
            attendance_pct REAL,
            assignment_score REAL,
            midterm_score REAL,
            participation REAL,
            previous_gpa REAL,
            predicted_class TEXT,
            confidence REAL,
            date_generated TEXT
        )
    """)

    q.execute("""
        CREATE TABLE IF NOT EXISTS uploaded_files(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_name TEXT,
            saved_path TEXT,
            rows_count INTEGER,
            date_uploaded TEXT
        )
    """)

    q.executemany(
        "INSERT OR IGNORE INTO users VALUES(?,?,?)",
        [
            ("admin", "admin123", "admin"),
            ("lecturer01", "pass1234", "lecturer"),
            ("adviser01", "pass1234", "adviser"),
        ],
    )
    c.commit()
    c.close()


def verify_user(username, password):
    c = con()
    row = c.execute(
        "SELECT username, role FROM users WHERE username=? AND password=?",
        (username, password),
    ).fetchone()
    c.close()
    return {"username": row[0], "role": row[1]} if row else None


def save_prediction(student_id, data, predicted_class, confidence=0):
    c = con()
    c.execute(
        """
        INSERT INTO predictions(
            student_id, attendance_pct, assignment_score, midterm_score,
            participation, previous_gpa, predicted_class, confidence,
            date_generated
        ) VALUES(?,?,?,?,?,?,?,?,?)
        """,
        (
            str(student_id),
            float(data["attendance_pct"]),
            float(data["assignment_score"]),
            float(data["midterm_score"]),
            float(data["participation"]),
            float(data["previous_gpa"]),
            str(predicted_class),
            float(confidence),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        ),
    )
    c.commit()
    c.close()


def save_batch_predictions(df):
    """Save all predictions from an uploaded CSV into the SQLite database."""
    required = [
        "attendance_pct",
        "assignment_score",
        "midterm_score",
        "participation",
        "previous_gpa",
        "predicted_class",
        "confidence",
    ]

    missing = [x for x in required if x not in df.columns]
    if missing:
        raise ValueError("Cannot save batch. Missing: " + ", ".join(missing))

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rows = []

    for index, row in df.iterrows():
        student_id = row.get("student_id", "")
        if student_id is None or str(student_id).strip() == "":
            student_id = f"CSV-{index + 1:04d}"

        rows.append(
            (
                str(student_id),
                float(row["attendance_pct"]),
                float(row["assignment_score"]),
                float(row["midterm_score"]),
                float(row["participation"]),
                float(row["previous_gpa"]),
                str(row["predicted_class"]),
                float(row["confidence"]),
                now,
            )
        )

    c = con()
    c.executemany(
        """
        INSERT INTO predictions(
            student_id, attendance_pct, assignment_score, midterm_score,
            participation, previous_gpa, predicted_class, confidence,
            date_generated
        ) VALUES(?,?,?,?,?,?,?,?,?)
        """,
        rows,
    )
    c.commit()
    c.close()
    return len(rows)


def save_uploaded_file(original_name, saved_path, rows_count):
    c = con()
    c.execute(
        """
        INSERT INTO uploaded_files(
            original_name, saved_path, rows_count, date_uploaded
        ) VALUES(?,?,?,?)
        """,
        (
            str(original_name),
            str(saved_path),
            int(rows_count),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        ),
    )
    c.commit()
    c.close()


def get_recent_predictions(limit=50):
    c = con()
    c.row_factory = sqlite3.Row
    rows = [
        dict(x)
        for x in c.execute(
            """
            SELECT student_id, attendance_pct, assignment_score,
                   midterm_score, participation, previous_gpa,
                   predicted_class, confidence, date_generated
            FROM predictions
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        )
    ]
    c.close()
    return rows


def get_prediction_counts():
    data = {x: 0 for x in ["At-Risk", "Average", "High-Achiever"]}
    c = con()
    for key, value in c.execute(
        "SELECT predicted_class, COUNT(*) FROM predictions GROUP BY predicted_class"
    ):
        if key in data:
            data[key] = value
    c.close()
    return data


def get_all_users():
    c = con()
    rows = [
        {"username": x[0], "role": x[1]}
        for x in c.execute("SELECT username, role FROM users")
    ]
    c.close()
    return rows


def add_user(username, password, role="lecturer"):
    c = con()
    try:
        c.execute(
            "INSERT INTO users VALUES(?,?,?)",
            (username, password, role),
        )
        c.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        c.close()


def delete_user(username):
    if username == "admin":
        return False
    c = con()
    c.execute("DELETE FROM users WHERE username=?", (username,))
    ok = c.total_changes > 0
    c.commit()
    c.close()
    return ok


def search_predictions(student_id):
    c = con(); c.row_factory = sqlite3.Row
    rows = [dict(x) for x in c.execute("SELECT student_id, attendance_pct, assignment_score, midterm_score, participation, previous_gpa, predicted_class, confidence, date_generated FROM predictions WHERE student_id LIKE ? ORDER BY id DESC", (f"%{student_id}%",))]
    c.close(); return rows


def get_all_predictions(limit=500):
    return get_recent_predictions(limit)


def clear_predictions():
    c=con(); c.execute("DELETE FROM predictions"); c.commit(); c.close()


def get_at_risk_predictions(limit=20):
    c=con(); c.row_factory=sqlite3.Row
    rows=[dict(x) for x in c.execute("SELECT student_id, attendance_pct, assignment_score, midterm_score, participation, previous_gpa, predicted_class, confidence, date_generated FROM predictions WHERE predicted_class='At-Risk' ORDER BY id DESC LIMIT ?",(limit,))]
    c.close(); return rows
