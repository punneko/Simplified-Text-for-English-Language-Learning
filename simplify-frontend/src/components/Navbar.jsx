import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import Sidebar from "./Sidebar";

const Navbar = ({ disableHamburger = false, zIndex = "z-50" }) => {
  const [isOpen, setIsOpen] = useState(false);
  const navigate = useNavigate();

  const toggleMenu = () => {
    if (!disableHamburger) setIsOpen(!isOpen);
  };

  const goToHome = () => navigate("/simplifier");

  return (
    <>
      <nav className={`fixed top-0 left-0 right-0 h-16 bg-white text-black p-4 flex items-center space-x-4 shadow-md ${zIndex}`}>
        <button
          className={`block focus:outline-none ${disableHamburger ? "opacity-50 cursor-not-allowed" : ""}`}
          onClick={toggleMenu}
          aria-label="Toggle menu"
        >
          <div className="space-y-1">
            <div className="w-6 h-0.5 bg-black"></div>
            <div className="w-6 h-0.5 bg-black"></div>
            <div className="w-6 h-0.5 bg-black"></div>
          </div>
        </button>

        <img src="/logo.png" alt="Logo" className="w-8 h-8 object-contain" />
        <div
          className="text-xl font-semibold cursor-pointer hover:text-sky-500 transition"
          onClick={goToHome}
        >
          SimplifyMe !
        </div>
      </nav>

      {!disableHamburger && <Sidebar isOpen={isOpen} toggleMenu={toggleMenu} />}
    </>
  );
};

export default Navbar;
