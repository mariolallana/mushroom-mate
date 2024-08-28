import React, { useEffect, useState } from 'react';
import axios from 'axios';

function MushroomSpeciesTable({ tipoBosqueId, selectedLocation }) {
  const [mushroomSpecies, setMushroomSpecies] = useState([]);

  useEffect(() => {
    if (tipoBosqueId && selectedLocation) {
      fetchMushroomSpecies(tipoBosqueId, selectedLocation);
    }
  }, [tipoBosqueId, selectedLocation]);

  const fetchMushroomSpecies = async (tipoBosqueId, selectedLocation) => {
    try {
      const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/mushroom-species-probabilities`, {
        params: { tipo_bosque_id: tipoBosqueId, location_id: selectedLocation }
      });
      setMushroomSpecies(response.data);
    } catch (error) {
      console.error('Error fetching mushroom species:', error);
    }
  };

  const renderProbabilityCell = (probability) => {
    let bgColor = '#e5e7eb'; // default gray for undefined or 0 probabilities
    if (probability === 'Low') bgColor = '#fecaca';
    else if (probability === 'Medium') bgColor = '#fed7aa';
    else if (probability === 'High') bgColor = '#bbf7d0';

    return (
      <td className="px-4 py-2 text-center" style={{ backgroundColor: bgColor }}>
        {probability}
      </td>
    );
  };

  return (
    <div className="bg-white shadow-md rounded-lg overflow-hidden">
      <h3 className="text-xl font-semibold p-4 bg-green-800 text-white">Mushroom Species</h3>
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Species Name</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Temperature Range (°C)</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Precipitation Range (mm)</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Optimal Altitude (m)</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Probability</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {mushroomSpecies.map(specie => (
              <tr key={specie.specie_id} className="hover:bg-gray-50">
                <td className="px-4 py-2 whitespace-nowrap">{specie.specie_name}</td>
                <td className="px-4 py-2 whitespace-nowrap">{`${specie.temp_min} - ${specie.temp_max}`}</td>
                <td className="px-4 py-2 whitespace-nowrap">{`${specie.prec_acc_min} - ${specie.prec_acc_max}`}</td>
                <td className="px-4 py-2 whitespace-nowrap">{`${specie.altura_optima_min} - ${specie.altura_optima_max}`}</td>
                {renderProbabilityCell(specie.probability)}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default MushroomSpeciesTable;