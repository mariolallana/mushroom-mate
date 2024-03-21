import React, { useState, useEffect } from 'react';

function LocationDropdown({ onLocationSelect }) {
  const [locations, setLocations] = useState([]);

  useEffect(() => {
    fetch(`${process.env.VITE_API_URL}/weather_data_grouped`)
      .then(response => response.json())
      .then(data => {
        console.log('Fetched locations:', data); // Log fetched data
        const locationNames = data.map(dataPoint => dataPoint.nombre);
        setLocations(locationNames);
      })
      .catch(error => console.error('Error fetching locations:', error));
  }, []);

  const handleLocationChange = (e) => {
    const selectedLocation = e.target.value;
    console.log('Selected location:', selectedLocation); // Log selected location
    onLocationSelect(selectedLocation);
  };

  return (
    <div className="relative">
      <label htmlFor="locations" className="block text-sm font-medium text-gray-700">Select a location:</label>
      <select id="locations" className="block w-full p-3 mt-1 border border-gray-300 rounded-md appearance-none focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500" onChange={handleLocationChange}>
        {locations.map((location, index) => (
          <option key={index} value={location} className="text-gray-900">{location}</option>
        ))}
      </select>
      <div className="absolute inset-y-0 right-0 flex items-center px-2 text-gray-700 pointer-events-none">
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7"></path>
        </svg>
      </div>
    </div>
  );
}

export default LocationDropdown;
