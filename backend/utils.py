import json
import sqlite3
import csv
from datetime import datetime


def validate_location(location):
    """Validate the location (basic placeholder)."""
    return bool(location.strip())  # Ensures the location is not empty


def validate_date_range(start_date, end_date):
    """Validate date ranges."""
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        return start <= end
    except ValueError:
        return False


def export_data(database, format):
    """Export data from the database to the specified format."""
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM weather_data')
    rows = cursor.fetchall()
    conn.close()

    file_path = None
    if format == 'json':
        file_path = 'weather_data.json'
        with open(file_path, 'w') as f:
            json.dump([dict(zip(['id', 'location', 'date_range', 'weather_info'], row)) for row in rows], f)
    elif format == 'csv':
        file_path = 'weather_data.csv'
        with open(file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'location', 'date_range', 'weather_info'])
            writer.writerows(rows)
    else:
        raise ValueError("Unsupported export format. Supported formats are: json, csv.")

    return file_path
