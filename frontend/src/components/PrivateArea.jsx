import React, { useState, useEffect } from "react";
import Header from "./Header";
import BackImage from "./BackImage";
import LeafletMap from "./LeafletMap";
import Footer from "./Footer";
import Legend from "./Legend";
import DataPointTable from "./DataPointTable";
import LocationDropdown from "./LocationDropdown";
import LineChart from "./LineChart";

function PrivateArea() {
  const [isLoginModalOpen, setLoginModalOpen] = useState(false);
  const [selectedLocation, setSelectedLocation] = useState("");
  const [selectedDate, setSelectedDate] = useState("");
  const [dataPoints, setDataPoints] = useState([]); // Define dataPoints state
  const [filteredDataPoints, setFilteredDataPoints] = useState([]);

  // Function to fetch data points
  useEffect(() => {
    // Fetch data points from the server
    fetch(`${process.env.VITE_API_URL}/api/weather_data_grouped`)
      .then(response => response.json())
      .then(data => {
        // Log the fetched data for verification
        console.log('Fetched data points:', data);
        // Set the fetched data to the dataPoints state
        setDataPoints(data);
      })
      .catch(error => console.error('Error fetching data points:', error));
  }, []);

  // Function to handle location selection
  const handleLocationSelect = (location) => {
    // Log the selected location for verification
    console.log('Selected location:', location);
    // Set the selected location to the state
    setSelectedLocation(location);
    
    // Filter dataPoints based on selected location
    const filteredData = dataPoints.filter(dataPoint => dataPoint.nombre === location);
    // Log the filtered data for verification
    console.log('Filtered data points:', filteredData);
    // Set the filtered data points to the state
    setFilteredDataPoints(filteredData);
  };

  return (
    <div>
      <Header />
      <BackImage />
      <div style={{ marginTop: "5cm" }}></div>
      <LocationDropdown onLocationSelect={handleLocationSelect} />
      <div style={{ marginTop: "1cm" }} className="flex flex-col items-center">
        <LeafletMap />
      </div>
      <div><Legend /></div>
      <div style={{ marginTop: "1cm" }}></div>
      <div>
        <DataPointTable dataPoints={filteredDataPoints} />
      </div>
      <div style={{ marginTop: "1cm" }}></div>
      <div>
        <LineChart dataPoints={filteredDataPoints} selectedLocation={selectedLocation} />
      </div>
      <div style={{ marginTop: "5cm" }}></div>
      <Footer />
    </div>
  );
}

export default PrivateArea;
