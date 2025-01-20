from flask import Flask, request, jsonify
import requests
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend-backend communication

# Database setup
DATABASE = 'weather.db'


def init_db():
    """Initialize the SQLite database."""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS weather_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                location TEXT NOT NULL,
                weather_info TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Error initializing database: {e}")


def execute_query(query, params=(), fetch=False):
    """Execute a query with optional parameters."""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute(query, params)
        if fetch:
            data = cursor.fetchall()
        else:
            data = None
        conn.commit()
        conn.close()
        return data
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None


# Initialize the database
init_db()

# Default route
@app.route('/')
def home():
    return "Welcome to the Weather App API! Use /api/weather or /api/weather-history."


# API to fetch weather data
@app.route('/api/weather', methods=['POST'])
def get_weather():
    try:
        data = request.json
        location = data.get('location')
        if not location:
            return jsonify({'error': 'Location is required'}), 400

        # OpenWeatherMap API key
        api_key = '8224e673233e1711f3ea4d57af392f9e'

        # Fetch weather from OpenWeatherMap API
        url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=imperial'
        response = requests.get(url)

        if response.status_code != 200:
            return jsonify({'error': 'Unable to fetch weather data'}), response.status_code

        weather_data = response.json()

        # Save to database
        execute_query('INSERT INTO weather_data (location, weather_info) VALUES (?, ?)',
                      (location, str(weather_data)))

        return jsonify(weather_data)

    except requests.RequestException as e:
        return jsonify({'error': 'Error fetching weather data from API', 'details': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500


# API to fetch weather history
@app.route('/api/weather-history', methods=['GET'])
def get_weather_history():
    try:
        rows = execute_query('SELECT * FROM weather_data', fetch=True)
        history = [{'id': row[0], 'location': row[1], 'weather_info': row[2]} for row in rows]
        return jsonify(history)
    except Exception as e:
        return jsonify({'error': 'Error retrieving weather history', 'details': str(e)}), 500


# API to fetch a specific weather record by ID
@app.route('/api/weather-history/<int:record_id>', methods=['GET'])
def get_weather_record(record_id):
    try:
        rows = execute_query('SELECT * FROM weather_data WHERE id = ?', (record_id,), fetch=True)
        if not rows:
            return jsonify({'message': 'Record not found'}), 404
        record = {'id': rows[0][0], 'location': rows[0][1], 'weather_info': rows[0][2]}
        return jsonify(record)
    except Exception as e:
        return jsonify({'error': 'Error retrieving record', 'details': str(e)}), 500


# API to update a weather record
@app.route('/api/weather-history/<int:record_id>', methods=['PUT'])
def update_weather_record(record_id):
    try:
        data = request.json
        location = data.get('location')
        weather_info = data.get('weather_info')
        if not location or not weather_info:
            return jsonify({'error': 'Both location and weather_info are required'}), 400

        result = execute_query('UPDATE weather_data SET location = ?, weather_info = ? WHERE id = ?',
                               (location, weather_info, record_id))
        if result is None:
            return jsonify({'message': 'Record not found or could not be updated'}), 404
        return jsonify({'message': f'Record with ID {record_id} updated successfully'})
    except Exception as e:
        return jsonify({'error': 'Error updating record', 'details': str(e)}), 500


# API to delete a weather record by ID
@app.route('/api/weather-history/<int:record_id>', methods=['DELETE'])
def delete_weather_record(record_id):
    try:
        result = execute_query('DELETE FROM weather_data WHERE id = ?', (record_id,))
        if result is None:
            return jsonify({'message': 'Record not found or could not be deleted'}), 404
        return jsonify({'message': f'Record with ID {record_id} deleted successfully'})
    except Exception as e:
        return jsonify({'error': 'Error deleting record', 'details': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
