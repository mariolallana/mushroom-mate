import React from "react";
import { Link } from "react-router-dom";
import logo from '../assets/logo.png';

function Header() {
  return (
    <header className="fixed top-0 left-0 w-full bg-green-800 bg-opacity-80 z-50 p-5 flex items-center justify-between">
      <div className="flex items-center">
        <img
          loading="lazy"
          src={logo}
          className="object-contain object-center h-36"
          alt="Logo"
        />
        <Link to="/">
          <div className="text-white text-4xl font-bold ml-24">
            <h3>MUSHROOM <br /> MATE</h3>
          </div>
        </Link>
      </div>
      <nav className="flex space-x-4">
        <Link to="/" className="text-white hover:text-green-200">HOME</Link>
        <Link to="/mush-finder" className="text-white hover:text-green-200">MUSH-FINDER</Link>
        <Link to="/mush-spot-exchange" className="text-white hover:text-green-200">MUSH-SPOT-EXCHANGE</Link>
        <Link to="/contact" className="text-white hover:text-green-200">CONTACT</Link>
      </nav>
    </header>
  );
}

export default Header;