import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

function RegisterModal({ isOpen, onClose }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleRegister = async () => {
    console.log("VITE_API_URL:", import.meta.env.VITE_API_URL); // Verification step
    
    // Send registration request to backend
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/register`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username,
          password,
        }),
      });
      const data = await response.json();
      console.log(data); // Handle the response from the server as needed
      // Redirect user to login page or another page after successful registration
      navigate("/login");
    } catch (error) {
      console.error("Error registering user:", error);
    }
  };

  return (
    <div
      className={`fixed inset-0 flex justify-center items-center bg-black bg-opacity-50 ${
        isOpen ? "" : "hidden"
      }`}
    >
      <div className="bg-white p-6 rounded shadow-lg">
        <h2 className="text-lg font-bold mb-4">Register</h2>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="block w-full px-3 py-2 rounded border border-gray-300 mb-2 text-black"
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="block w-full px-3 py-2 rounded border border-gray-300 mb-2 text-black"
        />
        <button
          className="bg-green-500 text-white px-4 py-2 rounded"
          onClick={handleRegister}
        >
          Register
        </button>
        <button
          className="text-gray-500 ml-2"
          onClick={onClose}
        >
          Cancel
        </button>
      </div>
    </div>
  );
}

export default RegisterModal;
