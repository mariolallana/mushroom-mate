import React, { useState, useEffect } from "react";
import { MapContainer, TileLayer, Polygon, Popup } from "react-leaflet";
import axios from "axios";
import "leaflet/dist/leaflet.css";
import { scaleOrdinal } from "d3-scale";
import { schemeCategory10 } from "d3-scale-chromatic";

function InteractiveMap({ onPolygonClick }) {
  const [forestData, setForestData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/forest-data`);
        const data = response.data;
        console.log(data); // Log the data to see its structure
        if (Array.isArray(data)) {
          setForestData(data);
        } else {
          console.error("API response is not an array:", data);
        }
      } catch (error) {
        console.error("Error fetching forest data:", error);
      }
    };
    fetchData();
  }, []);

  const colorScale = scaleOrdinal(schemeCategory10);

// Function to parse polygon WKT format into Leaflet-compatible coordinates
const parsePolygon = (polygonWKT) => {
  // Replace WKT "POLYGON" syntax and split pairs
  const coordinates = polygonWKT
    .replace("POLYGON ((", "")
    .replace("))", "")
    .split(", ")
    .map((pair) => {
      const [lng, lat] = pair.split(" ").map(Number);
      // Debugging: Print each parsed coordinate pair
      // console.log(`Parsed coordinates: [${lat}, ${lng}]`);
      // Ensure valid coordinates (filter out pairs that have NaN values)
      if (isNaN(lat) || isNaN(lng)) {
        console.error(`Invalid coordinate found: [${lat}, ${lng}]`);
        return null; // Indicate invalid coordinates
      }
      return [lat, lng]; // Return in [lat, lng] format
    })
    .filter((coord) => coord !== null); // Remove invalid pairs

  return coordinates;
};


  return (
    <MapContainer center={[40.624, -4.160]} zoom={13} style={{ height: '100vh', width: '100%' }}>
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
      {forestData.length > 0 && forestData.map((polygon, index) => (
        <Polygon
          key={index}
          positions={parsePolygon(polygon.polygon)}
          pathOptions={{ color: colorScale(polygon.tipo_id), fillOpacity: 0.5 }}
          eventHandlers={{
            click: () => {
              if (onPolygonClick) {
                onPolygonClick({
                  tipoBosqueId: polygon.tipo_id,
                  locationId: polygon.location_id  // Assuming `location_id` is a property you have
                });
              }
            }
          }}
        >
          <Popup>{`Tipo bosque: ${polygon.tipo_desc}, Altitud: ${polygon.altitude} m`}</Popup>
        </Polygon>
      ))}
    </MapContainer>
  );
}

export default InteractiveMap;