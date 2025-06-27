from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sporttracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    type = db.Column(db.String(120), nullable=False)
    distance = db.Column(db.Float)
    duration = db.Column(db.Float)  # minutes
    notes = db.Column(db.Text)

    def __repr__(self):
        return f"<Activity {self.type} on {self.date}>"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/activities')
def activities():
    all_activities = Activity.query.order_by(Activity.date.desc()).all()
    return render_template('activities.html', activities=all_activities)


@app.route('/add_activity', methods=['GET', 'POST'])
def add_activity():
    if request.method == 'POST':
        date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        type_ = request.form['type']
        distance = float(request.form.get('distance', 0))
        duration = float(request.form.get('duration', 0))
        notes = request.form.get('notes', '')
        activity = Activity(date=date, type=type_, distance=distance, duration=duration, notes=notes)
        db.session.add(activity)
        db.session.commit()
        return redirect(url_for('activities'))

    return render_template('add_activity.html')


@app.route('/fetch_garmin')
def fetch_garmin():
    """Example endpoint to fetch data from Garmin Connect"""
    username = os.getenv('GARMIN_USERNAME')
    password = os.getenv('GARMIN_PASSWORD')
    if not username or not password:
        return "Garmin credentials missing", 400
    try:
        from garminconnect import Garmin
    except Exception as e:
        return f"Garmin library not available: {e}", 500

    try:
        garmin = Garmin(username, password)
        garmin.login()
        activities = garmin.get_activities(0, 10)
        for act in activities:
            date = datetime.strptime(act['startTimeLocal'][:10], '%Y-%m-%d').date()
            type_ = act.get('activityType', 'Unknown')
            distance = act.get('distance', 0) / 1000  # convert to km
            duration = act.get('duration', 0) / 60
            activity = Activity(date=date, type=type_, distance=distance, duration=duration)
            # Avoid duplicates based on startTimeLocal
            if not Activity.query.filter_by(date=date, type=type_, distance=distance).first():
                db.session.add(activity)
        db.session.commit()
        return redirect(url_for('activities'))
    except Exception as e:
        return f"Garmin fetch failed: {e}", 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
