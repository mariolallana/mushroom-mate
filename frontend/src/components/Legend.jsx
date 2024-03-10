// Legend.jsx
import React from "react";
import { scaleLinear } from "d3-scale";

const Legend = () => {
  const colorScale = scaleLinear()
    .domain([0, 100]) // Input domain (total_prec values)
    .range(["red", "green"]); // Output range (colors)

  return (
    <div className="bg-white rounded-lg shadow-lg p-4 mt-8">
      <h2 className="text-lg font-semibold mb-2">Legend</h2>
      <div className="flex justify-between">
        <div className="flex items-center">
          <div className="w-4 h-4 rounded-full bg-grey mr-2"></div>
          <span className="text-sm text-gray-600">Low</span>
        </div>
        <div className="flex items-center">
          <div className="w-4 h-4 rounded-full bg-red mr-2"></div>
          <span className="text-sm text-gray-600">High</span>
        </div>
      </div>
      <div className="flex mt-4">
        <div
          className="h-4 w-full bg-gradient-to-r from-grey to-red rounded-lg"
          style={{
            backgroundImage: `linear-gradient(to right, ${colorScale(0)}, ${colorScale(
              100
            )})`,
          }}
        ></div>
      </div>
      <div className="flex justify-between mt-2">
        <span className="text-sm text-gray-600">0</span>
        <span className="text-sm text-gray-600">100</span>
      </div>
    </div>
  );
};

export default Legend;
