import React, { useState } from "react";
import Header from "./Header";
import BackImage from "./BackImage";
import HomePageLogin from "./HomePageLogin";
import HomePageThree from "./HomePageThree";
import LeafletMap from "./LeafletMap";
import Footer from "./Footer";
import LoginModal from "./LoginModal";
import Legend from "./Legend";
import DataPointTable from "./DataPointTable";
import LocationDropdown from "./LocationDropdown";

function PrivateArea() {
  const [isLoginModalOpen, setLoginModalOpen] = useState(false);
  const [selectedLocation, setSelectedLocation] = useState("");
  const [selectedDate, setSelectedDate] = useState("");

  const openLoginModal = () => setLoginModalOpen(true);
  const closeLoginModal = () => setLoginModalOpen(false);

  const [filteredDataPoints, setFilteredDataPoints] = useState([]);

  // Function to filter data points based on selected location and date
  const handleDataPointsChange = (dataPoints, selectedLocation, selectedDate) => {
    const filteredData = dataPoints.filter(
      (dataPoint) =>
        dataPoint.nombre === selectedLocation &&
        dataPoint.window_start === selectedDate
    );
    setFilteredDataPoints(filteredData);
  };

  return (
    <div>
      <Header />
      <BackImage />
      <div style={{ marginTop: "5cm" }}></div>
      <LocationDropdown onDataPointsChange={handleDataPointsChange} />
      <div style={{ marginTop: "5cm" }} className="flex flex-col items-center">
        <LeafletMap />
      </div>
      <div><Legend /></div>
      <div style={{ marginTop: "1cm" }}></div>
      <div>
      <DataPointTable dataPoints={filteredDataPoints} />
      </div>
      <div style={{ marginTop: "5cm" }}></div>
      <Footer />
    </div>
  );
}

export default PrivateArea;
