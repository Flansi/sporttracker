# Sport Tracker Flask App

Dies ist eine einfache Fitness-Webanwendung auf Basis von Flask. Sie zeigt einen Wochenplan und erlaubt das Speichern eigener Aktivitäten. Optional können Aktivitäten von einer Garmin-Uhr über die inoffizielle `garminconnect`-Bibliothek importiert werden.

## Setup

1. Python-Umgebung erstellen und Abhängigkeiten installieren
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Um Garmin-Daten zu importieren, müssen die Umgebungsvariablen `GARMIN_USERNAME` und `GARMIN_PASSWORD` gesetzt werden.

3. Anwendung starten
```bash
python app.py
```

Die App ist danach unter `http://localhost:5000` erreichbar.

## Datenbank
Die Anwendung verwendet SQLite (`sporttracker.db`). Beim ersten Start werden die Tabellen automatisch angelegt.

