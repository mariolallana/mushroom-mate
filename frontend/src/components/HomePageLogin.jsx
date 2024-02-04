import React, { useState } from "react";
import LoginModal from "./LoginModal"; // Adjust the path as needed
import { useNavigate } from "react-router-dom";

function HomePageLogin() {
  const [isLoginModalOpen, setLoginModalOpen] = useState(false);

  const openLoginModal = () => {
    setLoginModalOpen(true);
  };

  const closeLoginModal = () => {
    setLoginModalOpen(false);
  };

  return (
    <div className="flex flex-col items-center px-5 text-xl text-center text-white max-w-[723px]  mt-24">
      <header className="text-5xl max-md:max-w-full" aria-label="Welcome">
        Welcome to MushroomMate
      </header>
      <div
        className="self-stretch mt-16 w-full max-md:mt-10 max-md:max-w-full"
        aria-label="Description"
      >
        Explore the wonders of mushroom foraging in mountainous and forested
        areas
      </div>
      <form className="flex gap-5 justify-between items-stretch mt-11 w-full font-bold whitespace-nowrap max-w-[513px] max-md:flex-wrap max-md:mt-10 max-md:max-w-full">
        <button
          className="justify-center items-stretch px-6 py-3.5 bg-green-800 rounded shadow-sm max-md:px-5"
          aria-label="Login"
          type="button"
          onClick={openLoginModal}
        >
          Login
        </button>
        <button
          className="justify-center items-stretch px-10 py-4 bg-green-800 rounded shadow-sm max-md:px-5"
          aria-label="Register"
          type="button"
        >
          Register
        </button>
      </form>
      <LoginModal isOpen={isLoginModalOpen} onClose={closeLoginModal} />
    </div>
  );
}

export default HomePageLogin;
