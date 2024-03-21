// LoginModal.jsx

import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

function LoginModal({ isOpen, onClose }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, password }),
      });

      if (response.ok) {
        // Redirect to the PrivateArea page if login is successful
        navigate("/PrivateArea");
      } else {
        // Handle invalid credentials
        alert("Invalid credentials. Please try again.");
      }
    } catch (error) {
      console.error("Error logging in:", error);
    }
  };
  return (
    <div
      className={`fixed inset-0 flex items-center justify-center ${
        isOpen ? "visible" : "invisible"
      }`}
    >
      <div className="absolute inset-0 bg-black opacity-50"></div>
      <div className="z-10 bg-white p-8 rounded-md shadow-md">
        <h2 className="text-2xl font-bold mb-4">Login</h2>
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-600">User:</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="mt-1 p-2 border border-grey-300 rounded-md w-full text-black"
          />
        </div>
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-600">Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="mt-1 p-2 border border-gray-300 rounded-md w-full text-black"
          />
        </div>
        <button
          onClick={handleLogin}
          className="bg-green-500 text-green px-4 py-2 rounded-md"
        >
          Login
        </button>
        <button onClick={onClose} className="ml-2 text-gray-500">
          Close
        </button>
      </div>
    </div>
  );
}

export default LoginModal;
