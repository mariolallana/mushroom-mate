import React, { useEffect, useRef, useState } from 'react';
import Chart from 'chart.js/auto';
import axios from 'axios';

function LineChart({ selectedLocation }) {
  const chartRef = useRef(null);
  const [chart, setChart] = useState(null);

  useEffect(() => {
    if (selectedLocation) {
      fetchWeatherData();
    }
  }, [selectedLocation]);

  const fetchWeatherData = async () => {
    try {
      const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/weather-data-new?location_id=${selectedLocation}`);
      if (response.data) {
        updateChart(response.data);
      }
    } catch (error) {
      console.error('Error fetching weather data:', error);
    }
  };

  const updateChart = (weatherData) => {
    if (!weatherData || weatherData.length === 0) {
      console.log("No weather data available to plot.");
      return;
    }

    const ctx = chartRef.current.getContext('2d');
    if (chart) {
      chart.destroy();
    }

    const newChart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: weatherData.map(data => new Date(data.date).toLocaleDateString()),
        datasets: [
          {
            label: 'Total Precipitation',
            data: weatherData.map(data => data.prec ?? 0),
            backgroundColor: 'rgba(0, 123, 255, 0.8)', // Vibrant blue
            yAxisID: 'yPrecip',
          },
          {
            type: 'line',
            label: 'Max Temperature',
            data: weatherData.map(data => data.temp_max ?? 0),
            borderColor: 'rgba(255, 0, 0, 0.8)', // Vibrant red
            yAxisID: 'yTemp',
          },
          {
            type: 'line',
            label: 'Min Temperature',
            data: weatherData.map(data => data.temp_min ?? 0),
            borderColor: 'rgba(0, 255, 0, 0.8)', // Vibrant green
            yAxisID: 'yTemp',
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: {
            title: {
              display: true,
              text: 'Date',
              color: '#1F2937',
              font: { weight: 'bold' }
            },
            ticks: { color: '#4B5563' }
          },
          yTemp: {
            type: 'linear',
            position: 'left',
            title: {
              display: true,
              text: 'Temperature (°C)',
              color: '#1F2937',
              font: { weight: 'bold' }
            },
            ticks: { color: '#4B5563' }
          },
          yPrecip: {
            type: 'linear',
            position: 'right',
            title: {
              display: true,
              text: 'Precipitation (mm)',
              color: '#1F2937',
              font: { weight: 'bold' }
            },
            ticks: { color: '#4B5563' }
          }
        },
        plugins: {
          legend: {
            labels: { color: '#1F2937' }
          }
        }
      }
    });

    setChart(newChart);
  };

  return (
    <div className="bg-white shadow-md rounded-lg overflow-hidden">
      <h3 className="text-xl font-semibold p-4 bg-green-800 text-white">Weather Data</h3>
      <div className="p-4">
        <canvas ref={chartRef} style={{ width: '100%', height: '400px' }}></canvas>
      </div>
    </div>
  );
}

export default LineChart;