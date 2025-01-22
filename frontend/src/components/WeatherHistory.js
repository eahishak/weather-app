import axios from 'axios';
import React, { useEffect, useState } from 'react';

const WeatherHistory = () => {
  const [history, setHistory] = useState([]);
  const [error, setError] = useState('');

  const API_URL = process.env.REACT_APP_API_URL + '/weather-history';

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const response = await axios.get(API_URL);
      setHistory(response.data);
    } catch (err) {
      setError('Error fetching history.');
    }
  };

  const deleteRecord = async (id) => {
    try {
      await axios.delete(`${API_URL}/${id}`);
      fetchHistory(); // Refresh history after deletion
    } catch (err) {
      setError('Error deleting record.');
    }
  };

  return (
    <div>
      <h2>Weather History</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {history.length > 0 ? (
        <ul>
          {history.map((record) => (
            <li key={record.id}>
              {record.location} - {record.date_range}
              <button onClick={() => deleteRecord(record.id)} style={{ marginLeft: '1rem', color: 'red' }}>
                Delete
              </button>
            </li>
          ))}
        </ul>
      ) : (
        <p>No history available.</p>
      )}
    </div>
  );
};

export default WeatherHistory;
