import React, { useState, useEffect } from 'react';

function DataPointTable({ dataPoints }) {
  const [additionalData, setAdditionalData] = useState([]);

  // Function to fetch additional data for a given location name (nombre)
  const fetchAdditionalData = async (nombre) => {
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/weather-data-group-hist`);
      let text = await response.text();
      
      // Replace 'NaN' with null or "null" in the response text
      text = text.replace(/NaN/g, "null");
  
      const data = JSON.parse(text);
      // Filter data with the same 'nombre'
      const filteredData = data.filter(item => item.nombre === nombre);
      setAdditionalData(filteredData);
    } catch (error) {
      console.error('Error fetching additional data:', error);
    }
  };
  

  // Effect to fetch additional data when dataPoints change
  useEffect(() => {
    if (dataPoints && dataPoints.length > 0) {
      const uniqueNombres = [...new Set(dataPoints.map(item => item.nombre))];
      uniqueNombres.forEach(nombre => fetchAdditionalData(nombre));
    }
  }, [dataPoints]);

  // Check if dataPoints is not provided or empty
  if (!dataPoints || dataPoints.length === 0) {
    return <div>No data available</div>;
  }

  // Define the columns to display and their order
  const columns = ['Week', 'nombre', 'altitude', 'total_prec', 'media_diaria_prec'];

  // Render the table with data
  return (
    <div className="bg-white shadow-md rounded-lg overflow-hidden">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            {columns.map((column, index) => (
              <th
                key={index}
                scope="col"
                className={`px-6 py-3 text-center text-xs font-medium ${
                  index === 0 ? 'text-gray-700' : 'text-gray-500'
                } uppercase tracking-wider`}
              >
                {column}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {(additionalData.length > 0 ? additionalData : dataPoints).map((dataPoint, index) => (
            <tr key={index}>
              {columns.map((column, columnIndex) => (
                <td
                  key={columnIndex}
                  className={`px-6 py-4 whitespace-nowrap text-sm ${
                    columnIndex === 0 ? 'font-semibold' : 'text-gray-900'
                  }`}
                >
                  {columnIndex === 0 ? new Date(dataPoint['window_start']).toLocaleDateString() : dataPoint[column]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default DataPointTable;
