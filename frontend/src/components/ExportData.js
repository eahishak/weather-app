import React from 'react';

const ExportData = () => {
  const handleExport = (format) => {
    const API_URL = `${process.env.REACT_APP_API_URL}/export?format=${format}`;
    window.open(API_URL, '_blank');
  };

  return (
    <div>
      <h2>Export Weather Data</h2>
      <button onClick={() => handleExport('json')} style={{ marginRight: '1rem' }}>
        Export as JSON
      </button>
      <button onClick={() => handleExport('csv')}>Export as CSV</button>
    </div>
  );
};

export default ExportData;
