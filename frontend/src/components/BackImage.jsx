// BackImage.js

import React from "react";
import frondo from '../assets/fondo.jpg';

function BackImage() {
  return (
    <div className="fixed top-0 left-0 w-full h-full overflow-hidden z-[-1]">
      <img
        loading="lazy"
        src={frondo}
        className="object-fill w-full h-full"
        alt="Background"
      />
    </div>
  );
}

export default BackImage;
