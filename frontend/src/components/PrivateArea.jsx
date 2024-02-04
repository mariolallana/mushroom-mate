// PrivateArea.js
import React, { useState } from "react";
import Header from "./Header";
import BackImage from "./BackImage";
import HomePageLogin from "./HomePageLogin";
import HomePageThree from "./HomePageThree";
import LeafletMap from "./LeafletMap"; // Import the LeafletMap component
import Footer from "./Footer";
import LoginModal from "./LoginModal";

function PrivateArea() {
  const [isLoginModalOpen, setLoginModalOpen] = useState(false);

  const openLoginModal = () => setLoginModalOpen(true);
  const closeLoginModal = () => setLoginModalOpen(false);

  return (
    <div>
      <Header />
      <BackImage />
      <div style={{ marginTop: "5cm" }}></div>
      <div style={{ marginTop: "5cm" }} className="flex flex-col items-center">
      <LeafletMap />
      </div>
      <div style={{ marginTop: "5cm" }}></div>
      <Footer />
    </div>
  );
}

export default PrivateArea;
