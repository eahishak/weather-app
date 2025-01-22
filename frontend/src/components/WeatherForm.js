import axios from 'axios';
import React, { useState } from 'react';
import WeatherDisplay from './WeatherDisplay';

const WeatherForm = () => {
  const [location, setLocation] = useState('');
  const [weatherData, setWeatherData] = useState(null);
  const [forecastData, setForecastData] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const API_URL = process.env.REACT_APP_API_URL;

  const fetchWeather = async () => {
    setLoading(true);
    setError('');
    try {
      const currentWeather = await axios.post(`${API_URL}/weather`, { location });
      const forecastWeather = await axios.get(`https://api.openweathermap.org/data/2.5/forecast?q=${location}&appid=YOUR_API_KEY&units=metric`);

      setWeatherData(currentWeather.data);
      setForecastData(forecastWeather.data);
    } catch (err) {
      setError('Error fetching weather data.');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!location.trim()) {
      setError('Location is required.');
      return;
    }
    fetchWeather();
  };

  return (
    <div style={{ textAlign: 'center' }}>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Enter location"
          value={location}
          onChange={(e) => setLocation(e.target.value)}
          style={{ padding: '0.5rem', marginRight: '1rem', width: '300px' }}
        />
        <button type="submit" style={{ padding: '0.5rem 1rem', backgroundColor: '#4CAF50', color: '#fff' }}>
          Get Weather
        </button>
      </form>
      {loading && <p>Loading...</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <WeatherDisplay weatherData={weatherData} forecastData={forecastData} />
    </div>
  );
};

export default WeatherForm;
