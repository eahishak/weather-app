import React from 'react';

const WeatherForm = ({ location, setLocation, fetchWeather }) => {
    return (
        <div>
            <input
                type="text"
                value={location}
                onChange={(e) => setLocation(e.target.value)}
                placeholder="Enter city, zip code, or GPS coordinates"
                style={{ marginRight: '10px', padding: '5px' }}
            />
            <button onClick={fetchWeather} style={{ padding: '5px' }}>
                Get Weather
            </button>
        </div>
    );
};

export default WeatherForm;
