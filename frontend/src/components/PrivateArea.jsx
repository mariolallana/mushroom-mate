// PrivateArea.js
import React, { useState } from "react";
import Header from "./Header";
import BackImage from "./BackImage";
import HomePageLogin from "./HomePageLogin";
import HomePageThree from "./HomePageThree";
import LeafletMap from "./LeafletMap"; // Import the LeafletMap component
import Footer from "./Footer";
import LoginModal from "./LoginModal";
import Legend from "./Legend";
import DataPointTable from "./DataPointTable";
import LocationDropdown from "./LocationDropdown";

function PrivateArea() {
  const [isLoginModalOpen, setLoginModalOpen] = useState(false);

  const openLoginModal = () => setLoginModalOpen(true);
  const closeLoginModal = () => setLoginModalOpen(false);

  return (
    <div>
      <Header />
      <BackImage />
      <div style={{ marginTop: "5cm" }}></div>
      <LocationDropdown />
      <div style={{ marginTop: "5cm" }} className="flex flex-col items-center">
      <LeafletMap />

      </div>
      <div><Legend /></div>
      <div style={{ marginTop: "1cm" }}></div>
      <div><DataPointTable /></div>
      <div style={{ marginTop: "5cm" }}></div>
      <Footer />
    </div>
  );
}

export default PrivateArea;
