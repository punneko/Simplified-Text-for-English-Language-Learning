import React from "react";
import { Link, useNavigate } from "react-router-dom";

const Sidebar = ({
  isOpen,
  toggleMenu,
  alwaysOpen = false,
  customColor = "bg-white",
}) => {
  const navigate = useNavigate();
  const name =
    localStorage.getItem("name") || localStorage.getItem("email") || "User";

  const handleLogout = () => {
    localStorage.removeItem("token");
    toggleMenu && toggleMenu();
    alert("Are you sure?");
    navigate("/");
  };

  const sidebarClasses = `
    fixed top-16 left-0 h-[calc(100%-64px)] w-64 shadow-lg z-40
    ${customColor}
    transition-transform duration-300
    ${alwaysOpen ? "translate-x-0" : isOpen ? "translate-x-0" : "-translate-x-full"}
  `;

  return (
    <>
      <div className={sidebarClasses}>
        <div className="p-4 flex justify-between items-center border-b">
          <span className="text-lg font-semibold">
            Welcome <span className="text-sky-500">{name}</span>
          </span>
          {!alwaysOpen && (
            <button
              onClick={toggleMenu}
              aria-label="Close menu"
              className="cursor-pointer"
            >
              ✕
            </button>
          )}
        </div>

        <ul className="p-4 space-y-4">
          <li>
            <Link
              to="/history"
              className="block hover:text-sky-600"
              onClick={toggleMenu}
            >
              History
            </Link>
          </li>
          <li>
            <Link
              to="/manual"
              className="block hover:text-sky-600"
              onClick={toggleMenu}
            >
              User Manual
            </Link>
          </li>
          <li>
            <button
              onClick={handleLogout}
              className="block text-left w-full text-red-500 hover:text-red-700"
            >
              Logout
            </button>
          </li>
        </ul>
      </div>

      
      {!alwaysOpen && isOpen && (
        <div
          className="fixed top-16 left-0 w-full h-[calc(100%-64px)] bg-black opacity-30 z-30"
          onClick={toggleMenu}
        />
      )}
    </>
  );
};

export default Sidebar;
