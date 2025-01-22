import React from 'react';

const WeatherDisplay = ({ weatherData, forecastData }) => {
  if (!weatherData) {
    return null; // Don't display anything if there's no data
  }

  // Format sunrise and sunset times
  const formatTime = (timestamp) => {
    const date = new Date(timestamp * 1000); // Convert UNIX timestamp to milliseconds
    return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div style={{ marginTop: '2rem', textAlign: 'center', border: '1px solid #ccc', padding: '1rem', borderRadius: '8px' }}>
      <h2>Weather in {weatherData.name}</h2>
      <p>
        <strong>Temperature:</strong> {weatherData.main.temp}°C
      </p>
      <p>
        <strong>Feels Like:</strong> {weatherData.main.feels_like}°C
      </p>
      <p>
        <strong>Condition:</strong> {weatherData.weather[0].description}
      </p>
      <p>
        <strong>Humidity:</strong> {weatherData.main.humidity}%
      </p>
      <p>
        <strong>Wind Speed:</strong> {weatherData.wind.speed} m/s
      </p>
      <p>
        <strong>Sunrise:</strong> {formatTime(weatherData.sys.sunrise)}
      </p>
      <p>
        <strong>Sunset:</strong> {formatTime(weatherData.sys.sunset)}
      </p>

      {forecastData && (
        <>
          <h3>5-Day Forecast</h3>
          <div style={{ display: 'flex', justifyContent: 'center', gap: '1rem' }}>
            {forecastData.list.slice(0, 5).map((forecast, index) => (
              <div
                key={index}
                style={{
                  border: '1px solid #ccc',
                  padding: '1rem',
                  borderRadius: '8px',
                  width: '150px',
                  backgroundColor: '#f9f9f9',
                }}
              >
                <p><strong>{new Date(forecast.dt * 1000).toLocaleDateString()}</strong></p>
                <p>{forecast.weather[0].description}</p>
                <p>
                  <strong>Temp:</strong> {forecast.main.temp}°C
                </p>
                <p>
                  <strong>Wind:</strong> {forecast.wind.speed} m/s
                </p>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
};

export default WeatherDisplay;
