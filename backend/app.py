from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import sqlite3
import requests
from utils import validate_location, validate_date_range, export_data
import os
import logging

app = Flask(__name__)
CORS(app)

DATABASE = 'weather.db'
API_KEY = '8224e673233e1711f3ea4d57af392f9e'  # Replace with your OpenWeatherMap API Key

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def init_db():
    """Initialize the SQLite database."""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS weather_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                location TEXT NOT NULL,
                date_range TEXT NOT NULL,
                weather_info TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
        logging.info("Database initialized successfully.")
    except sqlite3.Error as e:
        logging.error(f"Error initializing database: {e}")


init_db()


@app.route('/api/weather', methods=['POST'])
def get_weather():
    """Fetch weather data and save to database."""
    try:
        data = request.json
        location = data.get('location')
        date_range = data.get('date_range', 'N/A')

        if not validate_location(location):
            return jsonify({'error': 'Invalid location'}), 400

        # Fetch weather data from OpenWeatherMap API
        weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}&units=metric'
        response = requests.get(weather_url)

        if response.status_code != 200:
            logging.error(f"Failed to fetch weather data: {response.text}")
            return jsonify({'error': 'Unable to fetch weather data', 'details': response.text}), response.status_code

        weather_data = response.json()

        # Save to database
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO weather_data (location, date_range, weather_info) VALUES (?, ?, ?)',
                       (location, date_range, str(weather_data)))
        conn.commit()
        conn.close()

        logging.info(f"Weather data for {location} saved successfully.")
        return jsonify(weather_data)
    except Exception as e:
        logging.error(f"Error in get_weather: {e}")
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500


@app.route('/api/weather-history', methods=['GET'])
def get_weather_history():
    """Fetch weather history from the database."""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM weather_data')
        rows = cursor.fetchall()
        conn.close()

        history = [{'id': row[0], 'location': row[1], 'date_range': row[2], 'weather_info': row[3]} for row in rows]
        return jsonify(history)
    except Exception as e:
        logging.error(f"Error fetching weather history: {e}")
        return jsonify({'error': 'Error fetching weather history', 'details': str(e)}), 500


@app.route('/api/weather-history/<int:record_id>', methods=['PUT'])
def update_weather_record(record_id):
    """Update a specific weather record."""
    try:
        data = request.json
        location = data.get('location')
        date_range = data.get('date_range')
        weather_info = data.get('weather_info')

        if not location or not weather_info or not validate_date_range(date_range):
            return jsonify({'error': 'Invalid input for update'}), 400

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('UPDATE weather_data SET location = ?, date_range = ?, weather_info = ? WHERE id = ?',
                       (location, date_range, weather_info, record_id))
        conn.commit()
        conn.close()

        logging.info(f"Weather record {record_id} updated successfully.")
        return jsonify({'message': 'Record updated successfully'})
    except Exception as e:
        logging.error(f"Error updating record: {e}")
        return jsonify({'error': 'Error updating record', 'details': str(e)}), 500


@app.route('/api/weather-history/<int:record_id>', methods=['DELETE'])
def delete_weather_record(record_id):
    """Delete a weather record."""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM weather_data WHERE id = ?', (record_id,))
        conn.commit()
        conn.close()

        logging.info(f"Weather record {record_id} deleted successfully.")
        return jsonify({'message': 'Record deleted successfully'})
    except Exception as e:
        logging.error(f"Error deleting record: {e}")
        return jsonify({'error': 'Error deleting record', 'details': str(e)}), 500


@app.route('/api/export', methods=['GET'])
def export_weather_data():
    """Export weather data to a specified format."""
    try:
        format = request.args.get('format', 'json')
        file_path = export_data(DATABASE, format)

        if not file_path:
            return jsonify({'error': 'Unsupported export format'}), 400

        response = send_file(file_path, as_attachment=True)
        os.remove(file_path)  # Cleanup exported file
        logging.info(f"Data exported as {format} successfully.")
        return response
    except Exception as e:
        logging.error(f"Error exporting data: {e}")
        return jsonify({'error': 'Error exporting data', 'details': str(e)}), 500


@app.route('/')
def home():
    """Home route."""
    return "Welcome to the Weather App API! Use /api/weather or /api/weather-history."


if __name__ == '__main__':
    try:
        app.run(debug=True)
    except Exception as e:
        logging.error(f"Error starting the server: {e}")
