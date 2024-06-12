import React, { useEffect, useState } from 'react';
import axios from 'axios';

function MushroomSpeciesTable({ tipoBosqueId, selectedLocation }) {
  const [mushroomSpecies, setMushroomSpecies] = useState([]);

  useEffect(() => {
    console.log('Selected Location:', selectedLocation); 
    if (tipoBosqueId && selectedLocation) { // Verifica que selectedLocation tenga un valor antes de hacer la solicitud
      fetchMushroomSpecies(tipoBosqueId, selectedLocation);
    }
  }, [tipoBosqueId, selectedLocation]); // Añade selectedLocation como una dependencia del efecto

  const fetchMushroomSpecies = async (tipoBosqueId, selectedLocation) => {
    try {
      const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/mushroom-species-probabilities`, {
        params: { tipo_bosque_id: tipoBosqueId, location_id: selectedLocation }
      });
      setMushroomSpecies(response.data);
      console.log('Fetched mushroom species and probabilities:', response.data);
    } catch (error) {
      console.error('Error fetching mushroom species:', error);
    }
  };

  const renderProbabilityCell = (probability) => {
    let bgColor = '#ccc'; // default gray for undefined or 0 probabilities
    if (probability === 'Low') bgColor = 'red';
    else if (probability === 'Medium') bgColor = 'orange';
    else if (probability === 'High') bgColor = 'green';

    return (
      <td style={{ backgroundColor: bgColor, color: '#fff', fontWeight: 'bold' }}>
        {probability}
      </td>
    );
  };

  return (
    <div className="rounded-lg overflow-hidden bg-green-800 bg-opacity-30 p-4 w-128 h-96">
      <h3>Mushroom Species</h3>
      <table>
        <thead>
          <tr>
            <th>Specie Name</th>
            <th>Description</th>
            <th>Temperature Max</th>
            <th>Temperature Min</th>
            <th>Precipitation Min</th>
            <th>Precipitation Max</th>
            <th>Optimal Altitude Min</th>
            <th>Optimal Altitude Max</th>
            <th>Probability</th> {/* New column header */}
          </tr>
        </thead>
        <tbody>
          {mushroomSpecies.map(specie => (
            <tr key={specie.specie_id}>  // Ensure specie_id is unique across all species
              <td>{specie.specie_name}</td>
              <td>{specie.specie_desc}</td>
              <td>{specie.temp_max}</td>
              <td>{specie.temp_min}</td>
              <td>{specie.prec_acc_min}</td>
              <td>{specie.prec_acc_max}</td>
              <td>{specie.altura_optima_min}</td>
              <td>{specie.altura_optima_max}</td>
              {renderProbabilityCell(specie.probability)}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default MushroomSpeciesTable;
