import React, { useState, useEffect } from 'react';

const MushroomList = ({ selectedLocation }) => {
  const [mushrooms, setMushrooms] = useState([]);

  useEffect(() => {
    const fetchMushrooms = async () => {
        try {
          // Include the selectedLocation in the API request
          const response = await fetch(`${import.meta.env.VITE_API_URL}/api/mushroom-species?location=${encodeURIComponent(selectedLocation)}`);
          if (response.ok) {
            const data = await response.json();
            setMushrooms(data);
          } else {
            console.error('Failed to fetch mushroom species');
          }
        } catch (error) {
          console.error('Error fetching mushroom species:', error);
        }
      };
      

    if (selectedLocation) {
      fetchMushrooms();
    }
  }, [selectedLocation]);

  return (
    <div className="bg-white shadow-md rounded-lg p-4">
      <table className="min-w-full">
        <thead>
          <tr className="text-left text-gray-700">
            <th>Nombre</th>
            <th>Foto</th>
            <th>Probabilidad</th>
            <th>Comestibilidad</th>
            <th>Localizacion</th>
          </tr>
        </thead>
        <tbody>
          {mushrooms.map((mushroom, index) => (
            <tr key={index} className="border-b">
              <td>{mushroom.nombre}</td>
              <td><img src={mushroom.foto} alt={mushroom.nombre} className="w-16 h-16"/></td>
              <td>{mushroom.probabilidad}</td>
              <td>{mushroom.comestible}</td>
              <td>{mushroom.location}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default MushroomList;
