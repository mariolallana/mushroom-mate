// InteractiveMap.jsx

import React, { useEffect, useState } from "react";
import { MapContainer, TileLayer, Circle, Popup } from "react-leaflet";
import axios from "axios";
import "leaflet/dist/leaflet.css";
import { scaleLinear } from "d3-scale";

function InteractiveMap() {
  const [weatherData, setWeatherData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(`${process.env.REACT_APP_API_URL}/weather_data_grouped`);
        setWeatherData(response.data);
      } catch (error) {
        console.error("Error fetching weather data:", error);
      }
    };

    fetchData();
  }, []);

  // Define a linear color scale
  const colorScale = scaleLinear()
    .domain([0, 100]) // Input domain (total_prec values)
    .range(["red", "green"]); // Output range (colors)

  return (
    <div className="relative w-full h-120 md:w-120 md:h-96 lg:w-120 lg:h-120 rounded-md overflow-hidden shadow-md z-10">
      <MapContainer
        center={[40.805, -4.09]}
        zoom={10}
        style={{ width: "100%", height: "100%" }}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {weatherData.map((dataPoint, index) => (
          <Circle
            key={index}
            center={[dataPoint.latitude, dataPoint.longitude]}
            radius={5000} // 10 km radius
            fillOpacity={0.5}
            color={colorScale(dataPoint.total_prec)}
          >
            <Popup position={[dataPoint.latitude, dataPoint.longitude]}>
              {`Location: ${dataPoint.nombre}, Total Precipitation: ${dataPoint.total_prec}`}
            </Popup>
          </Circle>
        ))}
      </MapContainer>
    </div>
  );
}

export default InteractiveMap;
