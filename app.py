from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from pathlib import Path

app = Flask(__name__)
DB_PATH = Path('activities.db')


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS activity (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                type TEXT,
                distance REAL,
                notes TEXT
            )"""
        )


def get_activities():
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute(
            "SELECT date, type, distance, notes FROM activity ORDER BY date DESC"
        )
        return [
            dict(date=row[0], type=row[1], distance=row[2], notes=row[3])
            for row in cur.fetchall()
        ]


def get_recent_activities(days: int = 14):
    """Return activities within the last ``days`` days."""
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute(
            """
            SELECT date, type, distance, notes FROM activity
            WHERE date >= date('now', ?)
            ORDER BY date DESC
            """,
            (f'-{days} days',),
        )
        return [
            dict(date=row[0], type=row[1], distance=row[2], notes=row[3])
            for row in cur.fetchall()
        ]


def get_average_distance(days: int = 14) -> float:
    """Return average distance of activities in the last ``days`` days."""
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute(
            "SELECT AVG(distance) FROM activity WHERE date >= date('now', ?)",
            (f'-{days} days',),
        )
        result = cur.fetchone()[0]
        return result or 0.0


def add_activity(date, type_, distance, notes):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO activity (date, type, distance, notes) VALUES (?, ?, ?, ?)",
            (date, type_, distance, notes),
        )
        conn.commit()


def fetch_garmin_activities(username: str, password: str):
    """Fetch activities from Garmin Connect. Requires valid credentials."""
    try:
        from garminconnect import Garmin

        api = Garmin(username, password)
        api.login()
        activities = api.get_activities(0, 5)
        data = []
        for a in activities:
            data.append(
                {
                    "date": a.get("startTimeLocal", "").split(" ")[0],
                    "type": a.get("activityType", {}).get("typeKey", ""),
                    "distance": a.get("distance", 0) / 1000,  # meters to km
                    "notes": "Garmin import",
                }
            )
        return data
    except Exception as err:
        print("Garmin import failed:", err)
        return []


@app.route("/")
def index():
    activities = get_activities()
    recent = get_recent_activities()
    avg_distance = get_average_distance()
    return render_template(
        "index.html",
        activities=activities,
        recent_activities=recent,
        avg_distance=avg_distance,
    )


@app.route("/add", methods=["GET", "POST"])
def add_activity_route():
    if request.method == "POST":
        date = request.form["date"]
        type_ = request.form["type"]
        distance = request.form["distance"]
        notes = request.form["notes"]
        add_activity(date, type_, distance, notes)
        return redirect(url_for("index"))
    return render_template("add.html")


@app.route("/import_garmin")
def import_garmin():
    # TODO: Replace with secure credential handling
    username = "your_garmin_username"
    password = "your_garmin_password"
    for act in fetch_garmin_activities(username, password):
        add_activity(act["date"], act["type"], act["distance"], act["notes"])
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
