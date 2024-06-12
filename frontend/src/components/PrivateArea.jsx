import React, { useState, useEffect } from "react";
import Header from "./Header";
import BackImage from "./BackImage";
import LeafletMap from "./LeafletMap";
import Footer from "./Footer";
import Legend from "./Legend";
import LocationDropdown from "./LocationDropdown";
import LineChart from "./LineChart";
import MushroomSpeciesTable from "./MushroomSpeciesTable";

function PrivateArea() {
  const [selectedLocation, setSelectedLocation] = useState(null);
  const [selectedPolygonTipoBosqueId, setSelectedPolygonTipoBosqueId] = useState(null);

  const onPolygonClick = (data) => {
    setSelectedLocation(data.locationId);
    setSelectedPolygonTipoBosqueId(data.tipoBosqueId);
  };

  console.log("Rendering PrivateArea, selectedPolygonTipoBosqueId:", selectedPolygonTipoBosqueId);

  return (
    <div>
      <Header />
      <BackImage />
      <div style={{ marginTop: "1cm" }}></div>
      <div style={{ position: 'relative', zIndex: 0 }}>
        <LeafletMap onPolygonClick={onPolygonClick} />
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
