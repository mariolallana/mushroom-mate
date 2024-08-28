import React, { useState, useEffect } from "react";
import axios from "axios";
import Header from "./Header";
import BackImage from "./BackImage";
import InteractiveMap from "./LeafletMap";
import Footer from "./Footer";
import Legend from "./Legend";
import LocationDropdown from "./LocationDropdown";
import LineChart from "./LineChart";
import MushroomSpeciesTable from "./MushroomSpeciesTable";
import FilterSelector from "./FilterSelector"; // Importa el nuevo componente

function PrivateArea() {
  const [selectedLocation, setSelectedLocation] = useState(null);
  const [selectedPolygonTipoBosqueId, setSelectedPolygonTipoBosqueId] = useState(null);
  const [selectedFilter, setSelectedFilter] = useState(""); // Estado para el filtro
  const [forestData, setForestData] = useState([]); // Estado para los datos del bosque

  const onPolygonClick = (data) => {
    setSelectedLocation(data.locationId);
    setSelectedPolygonTipoBosqueId(data.tipoBosqueId);
  };

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
    <div>
      <Header />
      <BackImage />
      <div style={{ marginTop: "6cm" }}></div>
      <FilterSelector forestData={forestData} selectedFilter={selectedFilter} setSelectedFilter={setSelectedFilter} />
      <div style={{ marginTop: "1cm" }}></div>
      <div style={{ position: 'relative', zIndex: 0, height: '60vh', width: '80%', margin: 'auto' }}>
  <InteractiveMap onPolygonClick={onPolygonClick} forestData={forestData} selectedFilter={selectedFilter} selectedLocation={selectedLocation} />
</div>
      <div style={{ marginTop: "1cm" }}></div>
      <div>
        <LineChart selectedLocation={selectedLocation} />
      </div>
      <div style={{ marginTop: "1cm" }}></div>
      {selectedPolygonTipoBosqueId && <MushroomSpeciesTable tipoBosqueId={selectedPolygonTipoBosqueId} selectedLocation={selectedLocation} />}
      <div style={{ marginTop: "5cm" }}></div>
      <Footer />
    </div>
  );
}

export default PrivateArea;
