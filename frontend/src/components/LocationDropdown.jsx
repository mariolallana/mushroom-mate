import React, { useState, useEffect } from 'react';

function LocationDropdown({ onDataPointsChange }) {
  const [locations, setLocations] = useState([]);
  const [dates, setDates] = useState([]);
  const [selectedLocation, setSelectedLocation] = useState('');
  const [selectedDate, setSelectedDate] = useState('');
  const [dataPoints, setDataPoints] = useState([]);

  useEffect(() => {
    fetch('http://localhost:5000/weather_data_grouped')
      .then(response => response.json())
      .then(data => {
        const locationNames = data.map(dataPoint => dataPoint.nombre);
        const uniqueDates = [...new Set(data.map(dataPoint => dataPoint.window_start))];
        setLocations(locationNames);
        setDates(uniqueDates);
        setDataPoints(data);
      })
      .catch(error => console.error('Error fetching locations, dates, and data points:', error));
  }, []);

  // Function to handle location change
  const handleLocationChange = (event) => {
    setSelectedLocation(event.target.value);
    onDataPointsChange(dataPoints, event.target.value, selectedDate);
  };

  // Function to handle date change
  const handleDateChange = (event) => {
    setSelectedDate(event.target.value);
    onDataPointsChange(dataPoints, selectedLocation, event.target.value);
  };

  return (
    <div className="grid grid-cols-2 gap-4">
      <div className="relative">
        <label htmlFor="locations" className="block text-sm font-medium text-gray-700">Select a location:</label>
        <select id="locations" value={selectedLocation} onChange={handleLocationChange} className="block w-full p-3 mt-1 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500">
          {locations.map((location, index) => (
            <option key={index} value={location} className="text-gray-900">{location}</option>
          ))}
        </select>
        <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700">
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7"></path>
          </svg>
        </div>
      </div>
      <div className="relative">
        <label htmlFor="dates" className="block text-sm font-medium text-gray-700">Select a date:</label>
        <select id="dates" value={selectedDate} onChange={handleDateChange} className="block w-full p-3 mt-1 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500">
          {dates.map((date, index) => (
            <option key={index} value={date} className="text-gray-900">{date}</option>
          ))}
        </select>
        <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700">
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7"></path>
          </svg>
        </div>
      </div>
    </div>
  );
}

export default LocationDropdown;
