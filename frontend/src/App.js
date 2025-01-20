import axios from 'axios';
import React, { useState } from 'react';
import WeatherDisplay from './components/WeatherDisplay';
import WeatherForm from './components/WeatherForm';

function App() {
    const [location, setLocation] = useState('');
    const [weather, setWeather] = useState(null);

    const fetchWeather = async () => {
        try {
            const response = await axios.post('http://127.0.0.1:5000/api/weather', {
                location,
            });
            setWeather(response.data);
        } catch (error) {
            alert('Error fetching weather data');
        }
    };

    return (
        <div style={{ padding: '20px' }}>
            <h1>Weather App</h1>
            <WeatherForm location={location} setLocation={setLocation} fetchWeather={fetchWeather} />
            <WeatherDisplay weather={weather} />
        </div>
    );
}

export default App;
