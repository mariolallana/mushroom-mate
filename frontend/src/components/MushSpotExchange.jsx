import React, { useState } from 'react';
import Header from './Header';
import Footer from './Footer';
import BackImage from "./BackImage";

function MushSpotExchange() {
  const [spots, setSpots] = useState([
    { id: 1, location: 'Pine Forest, North Ridge', price: 50, description: 'Excellent spot for chanterelles' },
    { id: 2, location: 'Oak Grove, East Valley', price: 75, description: 'Rich in porcini mushrooms' },
    { id: 3, location: 'Birch Woods, West Hills', price: 60, description: 'Great for morel hunting' },
  ]);

  const [newSpot, setNewSpot] = useState({ location: '', price: '', description: '' });

  const handleInputChange = (e) => {
    setNewSpot({ ...newSpot, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setSpots([...spots, { id: spots.length + 1, ...newSpot, price: Number(newSpot.price) }]);
    setNewSpot({ location: '', price: '', description: '' });
  };

  return (
    <div className="min-h-screen bg-green-50">
      <Header />
      <BackImage />
      <div className="container mx-auto mt-24 p-8">
        <h1 className="text-4xl font-bold text-green-800 mb-8">Mushroom Spot Exchange</h1>
        <p className="text-xl text-gray-700 mb-8">
          Welcome to the Mushroom Spot Exchange! Here, foragers can offer and discover prime mushroom hunting locations.
        </p>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div>
            <h2 className="text-2xl font-semibold text-green-700 mb-4">Available Spots</h2>
            <div className="space-y-4">
              {spots.map(spot => (
                <div key={spot.id} className="bg-white p-4 rounded-lg shadow">
                  <h3 className="text-lg font-semibold text-green-600">{spot.location}</h3>
                  <p className="text-gray-600">{spot.description}</p>
                  <p className="text-green-500 font-bold mt-2">${spot.price}</p>
                  <button className="mt-2 bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600">
                    Purchase Access
                  </button>
                </div>
              ))}
            </div>
          </div>
          
          <div>
            <h2 className="text-2xl font-semibold text-green-700 mb-4">Offer Your Spot</h2>
            <form onSubmit={handleSubmit} className="bg-white p-6 rounded-lg shadow">
              <div className="mb-4">
                <label htmlFor="location" className="block text-green-700 mb-2">Location</label>
                <input
                  type="text"
                  id="location"
                  name="location"
                  value={newSpot.location}
                  onChange={handleInputChange}
                  className="w-full p-2 border border-green-300 rounded"
                  required
                />
              </div>
              <div className="mb-4">
                <label htmlFor="price" className="block text-green-700 mb-2">Price ($)</label>
                <input
                  type="number"
                  id="price"
                  name="price"
                  value={newSpot.price}
                  onChange={handleInputChange}
                  className="w-full p-2 border border-green-300 rounded"
                  required
                />
              </div>
              <div className="mb-4">
                <label htmlFor="description" className="block text-green-700 mb-2">Description</label>
                <textarea
                  id="description"
                  name="description"
                  value={newSpot.description}
                  onChange={handleInputChange}
                  className="w-full p-2 border border-green-300 rounded"
                  required
                ></textarea>
              </div>
              <button type="submit" className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600">
                Offer Spot
              </button>
            </form>
          </div>
        </div>
      </div>
      <Footer />
    </div>
  );
}

export default MushSpotExchange;