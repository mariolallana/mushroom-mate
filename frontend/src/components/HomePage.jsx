// HomePage.js
import React from "react";
import Header from "./Header";
import BackImage from "./BackImage";
import HomePageLogin from "./HomePageLogin";
import HomePageThree from "./HomePageThree";
import LeafletMap from "./LeafletMap"; // Import the LeafletMap component
import Footer from "./Footer";

function HomePage() {

  return (
    <div>
      <Header />
      <BackImage />
      <div style={{ marginTop: "5cm" }}></div>
      <div className="flex flex-col items-center">
      <HomePageLogin />
      </div>
      <div style={{ marginTop: "5cm" }}></div>
      <HomePageThree />
      <div style={{ marginTop: "5cm" }}></div>
      <Footer />
    </div>
  );
}

export default HomePage;
