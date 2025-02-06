const API_URL = process.env.REACT_APP_API_URL;

export const fetchWeather = async (location) => {
  try {
    const response = await fetch(`${API_URL}/api/weather`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ location }),
    });
    if (!response.ok) {
      throw new Error('Failed to fetch weather data');
    }
    return response.json();
  } catch (error) {
    console.error('Error fetching weather:', error);
    throw error;
  }
};

export const fetchWeatherHistory = async () => {
  try {
    const response = await fetch(`${API_URL}/api/weather-history`);
    if (!response.ok) {
      throw new Error('Failed to fetch weather history');
    }
    return response.json();
  } catch (error) {
    console.error('Error fetching weather history:', error);
    throw error;
  }
};
