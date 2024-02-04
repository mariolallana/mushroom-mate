// Header.js

import React from "react";
import { Link } from "react-router-dom"; // Import Link from react-router-dom
import logo from '../assets/logo.png';

function Header() {
  return (
    <header className="fixed top-0 left-0 w-full bg-green-800 bg-opacity-60 p-5 flex items-center justify-between">
        <img
          loading="lazy"
          src={logo}
          className="object-contain object-center h-36"
          alt="Logo"
        />
      <Link to="/"> {/* Use Link for navigation */}
        <div className="text-white text-4xl font-bold ml-24">
          <h3>MUSHROOM <br /> MATE</h3>
        </div>
      </Link>
    </header>
  );
}

export default Header;
