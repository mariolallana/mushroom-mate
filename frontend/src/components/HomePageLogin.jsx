import React, { useState } from "react";
import LoginModal from "./LoginModal";
import RegisterModal from "./RegisterModal";
import { useNavigate } from "react-router-dom";

function HomePageLogin() {
  const [isLoginModalOpen, setLoginModalOpen] = useState(false);
  const [isRegisterModalOpen, setRegisterModalOpen] = useState(false); // State for RegisterModal
  const navigate = useNavigate();

  const openLoginModal = () => {
    setLoginModalOpen(true);
  };

  const closeLoginModal = () => {
    setLoginModalOpen(false);
  };

  const openRegisterModal = () => {
    setRegisterModalOpen(true);
  };

  const closeRegisterModal = () => {
    setRegisterModalOpen(false);
  };

  const handleRegister = async (username, password) => {
    // Send registration request to backend
    try {
      const response = await fetch("${process.env.REACT_APP_API_URL}/register", {
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
    <div>
      <div className="rounded-lg bg-white p-10">
        <div className="text-center text-5xl mb-8">Welcome to MushroomMate</div>
        <div className="text-center text-xl mb-8">
          Explore the wonders of mushroom foraging in mountainous and forested areas
        </div>
        <div className="flex justify-between">
          <button
            className="px-6 py-3.5 bg-green-800 rounded shadow-sm text-white font-bold"
            onClick={openLoginModal}
          >
            Login
          </button>
          <button
            className="px-10 py-4 bg-green-800 rounded shadow-sm text-white font-bold"
            onClick={openRegisterModal}
          >
            Register
          </button>
        </div>
      </div>
      <LoginModal isOpen={isLoginModalOpen} onClose={closeLoginModal} />
      <RegisterModal isOpen={isRegisterModalOpen} onClose={closeRegisterModal} />
    </div>
  );
}

export default HomePageLogin;
