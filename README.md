# Sporttracker

## Setup
1. Install dependencies:
```bash
pip install -r requirements.txt
```
2. Set the `GARMIN_KEY` environment variable. Generate a key with:
```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```
Then export it:
```bash
export GARMIN_KEY=your_generated_key  # on Windows use `set`
```
3. Run the application:
```bash
python app.py
```
