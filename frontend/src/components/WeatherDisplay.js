import React from 'react';

const WeatherDisplay = ({ weather }) => {
    if (!weather) return null;

    return (
        <div style={{ marginTop: '20px' }}>
            <h3>Weather in {weather.name}</h3>
            <p>Temperature: {weather.main.temp} °F</p>
            <p>Condition: {weather.weather[0].description}</p>
            <p>Humidity: {weather.main.humidity}%</p>
            <p>Wind Speed: {weather.wind.speed} mph</p>
        </div>
    );
};

export default WeatherDisplay;
