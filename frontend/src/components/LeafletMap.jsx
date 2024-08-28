import React, { useState, useEffect, useRef } from "react";
import { MapContainer, TileLayer, useMap } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import "leaflet.markercluster";
import "leaflet.markercluster/dist/MarkerCluster.css";
import "leaflet.markercluster/dist/MarkerCluster.Default.css";
import axios from "axios";
import { scaleOrdinal } from "d3-scale";
import { schemeCategory10 } from "d3-scale-chromatic";

const MapContent = ({ onPolygonClick, forestData, selectedFilter, selectedMunicipio, selectedLocation }) => {
  const map = useMap();
  const colorScale = scaleOrdinal(schemeCategory10);
  const [selectedPolygon, setSelectedPolygon] = useState(null);

  useEffect(() => {
    const markers = L.markerClusterGroup();

    const filteredForestData = forestData.filter(polygon => {
      return (
        (!selectedFilter || polygon.tipo_desc === selectedFilter) &&
        (!selectedMunicipio || polygon.municipio === selectedMunicipio)
      );
    });

    filteredForestData.forEach(polygon => {
      const isSelected = polygon.location_id === selectedLocation;
      const polygonLayer = L.polygon(parsePolygon(polygon.polygon), {
        color: isSelected ? '#ff0000' : colorScale(polygon.tipo_id),
        fillOpacity: 0.5
      }).on('click', () => {
        if (onPolygonClick) {
          onPolygonClick({
            tipoBosqueId: polygon.tipo_id,
            locationId: polygon.location_id
          });
        }
        if (selectedPolygon) {
          selectedPolygon.setStyle({ color: colorScale(selectedPolygon.options.data.tipo_id) });
        }
        polygonLayer.setStyle({ color: '#ff0000' });
        setSelectedPolygon(polygonLayer);
      }).bindPopup(`Tipo bosque: ${polygon.tipo_desc}, Altitud: ${polygon.altitude} m`);

      polygonLayer.options.data = polygon;
      markers.addLayer(polygonLayer);

      if (isSelected) {
        setSelectedPolygon(polygonLayer);
        map.fitBounds(polygonLayer.getBounds());
      }
    });

    map.addLayer(markers);

    if (selectedPolygon) {
      const animate = () => {
        selectedPolygon.setStyle({ fillOpacity: 0.8 });
        setTimeout(() => {
          selectedPolygon.setStyle({ fillOpacity: 0.5 });
        }, 500);
      };

      const intervalId = setInterval(animate, 1000);

      return () => {
        clearInterval(intervalId);
        map.removeLayer(markers);
      };
    }

    return () => {
      map.removeLayer(markers);
    };
  }, [forestData, selectedFilter, selectedMunicipio, map, onPolygonClick, selectedLocation]);

  const parsePolygon = (polygonWKT) => {
    const coordinates = polygonWKT
      .replace("POLYGON ((", "")
      .replace("))", "")
      .split(", ")
      .map((pair) => {
        const [lng, lat] = pair.split(" ").map(Number);
        if (isNaN(lat) || isNaN(lng)) {
          console.error(`Invalid coordinate found: [${lat}, ${lng}]`);
          return null;
        }
        return [lat, lng];
      })
      .filter((coord) => coord !== null);

    return coordinates;
  };

  return null;
};

function InteractiveMap({ onPolygonClick, selectedFilter, selectedMunicipio, selectedLocation }) {
  const [forestData, setForestData] = useState([]);
  const mapRef = useRef(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/forest-data`);
        const data = response.data;
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

  return (
    <MapContainer
      center={[40.873, -3.819]}
      zoom={12}
      style={{ height: '60vh', width: '80%', margin: 'auto' }}
      whenCreated={mapInstance => { mapRef.current = mapInstance; }}
    >
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
      <MapContent 
        onPolygonClick={onPolygonClick} 
        forestData={forestData} 
        selectedFilter={selectedFilter} 
        selectedMunicipio={selectedMunicipio}
        selectedLocation={selectedLocation}
      />
    </MapContainer>
  );
}

export default InteractiveMap;
