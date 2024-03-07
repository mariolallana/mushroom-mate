import React, { useEffect, useState } from "react";
import axios from "axios";

function DataPointTable() {
  const [weatherData, setWeatherData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get("http://localhost:5000/weather_data_grouped");
        setWeatherData(response.data);
      } catch (error) {
        console.error("Error fetching weather data:", error);
      }
    };

    fetchData();
  }, []);

  return (
    <div className="bg-white shadow-md rounded-lg overflow-hidden">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            <th scope="col" className="px-6 py-3 text-middle text-xs font-medium text-gray-500 uppercase tracking-wider">
              Location
            </th>
            <th scope="col" className="px-6 py-3 text-middle text-xs font-medium text-gray-500 uppercase tracking-wider">
              Total Precipitation
            </th>
            <th scope="col" className="px-6 py-3 text-middle text-xs font-medium text-gray-500 uppercase tracking-wider">
              Window start
            </th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {weatherData.map((dataPoint, index) => (
            <tr key={index}>
              <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                {dataPoint.nombre}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {dataPoint.total_prec}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {dataPoint.window_start}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default DataPointTable;
