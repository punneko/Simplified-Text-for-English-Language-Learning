import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";

const Simplifier = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [inputText, setInputText] = useState("");
  const navigate = useNavigate();

  const toggleSidebar = () => setSidebarOpen(!sidebarOpen);

  const handleSimplify = () => {
    if (!inputText.trim()) return;
    navigate(`/result?text=${encodeURIComponent(inputText)}`);
  };

  return (
    <div className="relative fredoka-font min-h-screen bg-gradient-to-br from-sky-200 via-blue-100 to-white pt-16 overflow-hidden">

      
      <div className="absolute top-24 left-24 w-80 h-80 bg-sky-300 rounded-full blur-3xl opacity-30"></div>
      <div className="absolute bottom-24 right-24 w-80 h-80 bg-blue-300 rounded-full blur-3xl opacity-30"></div>

      <Navbar toggleSidebar={toggleSidebar} />
      <Sidebar
        isOpen={sidebarOpen}
        toggleMenu={toggleSidebar}
        customColor="bg-sky-100"
      />

      <main
        className={`relative z-10 transition-transform duration-300 ${
          sidebarOpen ? "translate-x-64" : "translate-x-0"
        }`}
      >
        <div className="flex flex-col items-center justify-center min-h-[85vh] px-6 text-center">

         
          <h1 className="text-4xl font-bold mb-4 text-gray-800">
            Text Simplifier Tool
          </h1>

          <p className="text-gray-600 max-w-xl mb-10">
            วางข้อความภาษาอังกฤษที่ต้องการ ระบบจะช่วยปรับให้อ่านง่ายขึ้น
          </p>

        
          <div className="w-full max-w-3xl bg-white/80 backdrop-blur-xl p-8 rounded-3xl shadow-2xl border border-white/40">

            <textarea
              className="w-full h-52 p-4 border border-gray-200 rounded-xl focus:ring-2 focus:ring-sky-400 outline-none resize-none"
              placeholder="กรอกข้อความที่นี่..."
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
            />

          
            <div className="flex justify-between items-center mt-4 text-sm text-gray-500">
              <span>{inputText.length} characters</span>
              <button
                onClick={() => setInputText("")}
                className="hover:text-red-500 transition"
              >
                Clear
              </button>
            </div>

          
            <button
              onClick={handleSimplify}
              className="mt-6 px-8 py-3 bg-sky-500 text-white rounded-xl shadow-md hover:bg-sky-600 hover:scale-105 transition-all duration-200"
            >
              Simplify
            </button>
          </div>

        </div>
      </main>
    </div>
  );
};

export default Simplifier;