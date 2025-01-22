import React from 'react';
import ExportData from './components/ExportData';
import VideoAndMap from './components/VideoAndMap';
import WeatherForm from './components/WeatherForm';
import WeatherHistory from './components/WeatherHistory';

function App() {
  return (
    <div>
      <header style={{ textAlign: 'center', padding: '1rem', backgroundColor: '#4CAF50', color: '#fff' }}>
        <h1>Weather App</h1>
        <p>Advanced Weather Tracking and Insights</p>
      </header>
      <main style={{ padding: '2rem' }}>
        <WeatherForm />
        <WeatherHistory />
        <ExportData />
        <VideoAndMap />
      </main>
    </div>
  );
}

export default App;
