import React, { useEffect, useRef, useState } from 'react';
import Chart from 'chart.js/auto';
import axios from 'axios';

function LineChart({ selectedLocation }) {
  const chartRef = useRef(null);
  const [chart, setChart] = useState(null);

  const fetchWeatherData = async () => {
    try {
      const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/weather-data-new?location_id=${selectedLocation}`);
      // Check if the data needs to be cleaned up
      if (typeof response.data === 'string') {
        const cleanedData = response.data.replace(/NaN/g, 'null');
        const weatherData = JSON.parse(cleanedData);
        updateChart(weatherData);
      } else {
        // If the data is already parsed as an object and does not contain strings needing replacement
        const weatherData = response.data;
        updateChart(weatherData);
      }
    } catch (error) {
      console.error('Error fetching weather data:', error);
    }
  };
  

  useEffect(() => {
    fetchWeatherData();
  }, [selectedLocation]);
  

  // Function to update the chart with new data
  const updateChart = (weatherData) => {
    // Ensure weather data is available
    if (!weatherData || weatherData.length === 0) {
      console.log("No weather data available to plot.");
      return;
    }
  
    console.log("Weather data for chart:", weatherData);  

    // Parse dates and prepare data for the chart
    const labels = weatherData.map(data => new Date(data.date).toLocaleDateString());
    //console.log("Chart labels (dates):", labels);
    const totalPrecData = weatherData.map(data => data.prec ?? 0);
    const maxTmedData = weatherData.map(data => data.temp_max ?? 0);
    const minTmedData = weatherData.map(data => data.temp_min ?? 0);
  
    // Access the canvas context
    const ctx = chartRef.current.getContext('2d');
    if (!ctx) {
      console.error("Canvas context is not available.");
      return;
    }
  
    // Destroy any existing chart instance
    if (chart) {
      chart.destroy();
    }
  
    // Create a new chart instance with updated data
    const newChart = new Chart(ctx, {
      data: {
        labels,
        datasets: [
          {
            type: 'bar', // Specify the type for this dataset
            label: 'Total Precipitation',
            data: totalPrecData,
            backgroundColor: 'rgba(54, 162, 235, 0.8)', //54, 162, 235
            yAxisID: 'yPrecip', // Reference the axis ID for precipitation
          },
          {
            type: 'line', // Specify the type for this dataset
            label: 'Max Temperature',
            data: maxTmedData,
            borderColor: 'rgba(255, 99, 132, 0.8)',
            fill: false,
            yAxisID: 'yTemp', // Reference the axis ID for temperature
          },
          {
            type: 'line', // Specify the type for this dataset
            label: 'Min Temperature',
            data: minTmedData,
            borderColor: 'rgba(255, 255, 0, 0.5)',
            fill: false,
            yAxisID: 'yTemp', // Reference the axis ID for temperature
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: {
            beginAtZero: true,
            ticks: {
              color: 'white',  // This changes the color of the x-axis tick labels
              font: {
                size: 14, // Adjust the font size if needed
              },
            },
            title: {
              display: true,
              text: 'Date'
            }
          },
          yTemp: { // Configuration for the temperature axis
            type: 'linear',
            display: true,
            position: 'left',
            ticks: {
              color: 'white',  // This changes the color of the x-axis tick labels
              font: {
                size: 14, // Adjust the font size if needed
              },
            },
            title: {
              display: true,
              text: 'Temperature (°C)',
              color: 'white',
            },
            suggestedMin: 0, // Adjust if necessary
          },
          yPrecip: { // Configuration for the precipitation axis
            type: 'linear',
            display: true,
            position: 'right',
            ticks: {
              color: 'white',  // This changes the color of the x-axis tick labels
              font: {
                size: 14, // Adjust the font size if needed
              },
            },
            title: {
              display: true,
              text: 'Precipitation (mm)',
              color: 'white',
            },
            suggestedMin: 0, // Adjust if necessary
            grid: {
              drawOnChartArea: false, // Ensure that the grid lines do not overlap with the temperature axis
            },
          }
        },
        plugins: {
          legend: {
            labels: {
              color: 'white',
              font: {
                size: 14,
              },
            },
          },
          tooltip: {
            callbacks: {
              label: function(context) {
                return `${context.dataset.label}: ${context.parsed.y}`;
              },
            },
          },
        },
      },
    });
  
    // Save the new chart instance
    setChart(newChart);
  };
  

  return (
    <div className="rounded-lg overflow-hidden bg-green-800 bg-opacity-30 p-4 w-128 h-96">
      <canvas ref={chartRef}></canvas>
    </div>
  );
}

export default LineChart;
