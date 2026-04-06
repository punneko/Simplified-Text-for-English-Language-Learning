import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const CheckItem = ({ isValid, label }) => (
  <div className="flex items-center space-x-2 text-xs">
    <span
      className={`flex items-center justify-center w-4 h-4 rounded-full text-white text-[10px]
        ${isValid ? "bg-green-500" : "bg-red-500"}`}
    >
      {isValid ? "✓" : "✕"}
    </span>
    <span className={isValid ? "text-green-600" : "text-red-500"}>
      {label}
    </span>
  </div>
);

const Signup = () => {
  const navigate = useNavigate();

  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");

  const checks = {
    length: password.length >= 8,
    uppercase: /[A-Z]/.test(password),
    lowercase: /[a-z]/.test(password),
    match: confirmPassword.length > 0 && password === confirmPassword,
  };

  const isPasswordValid =
    checks.length && checks.uppercase && checks.lowercase;

  const isFormValid = isPasswordValid && checks.match;

  const handleSubmit = (e) => {
    e.preventDefault();
    setError("");

    const formData = new FormData(e.target);
    const name = formData.get("name");
    const email = formData.get("email");

    if (!isFormValid) {
      setError("Please fix the errors before submitting.");
      return;
    }

    fetch("http://localhost:5000/api/auth/signup", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, email, password }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data?.user_id) {
          localStorage.setItem("user_id", data.user_id);
          localStorage.setItem("name", data.name);
          localStorage.setItem("email", data.email);
          navigate("/simplifier");
        } else {
          setError(data?.error || "Signup failed");
        }
      })
      .catch(() => {
        setError("Something went wrong. Please try again.");
      });
  };

  const handleSignIn = () => {
    navigate("/");
  };

  return (
    <div className="fredoka-font min-h-screen flex items-center justify-center bg-gradient-to-b from-sky-200 via-blue-100 to-white">
      <div className="bg-white/90 backdrop-blur-md p-6 rounded-3xl shadow-xl w-full max-w-sm border border-sky-100">

        <h2 className="text-3xl font-bold mb-8 text-center text-grey-800">
          Create an Account
        </h2>

        <form onSubmit={handleSubmit} className="space-y-5">

          <input
            type="text"
            name="name"
            placeholder="Username"
            className="w-full border border-sky-200 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-sky-400 transition"
            required
          />

          <input
            type="email"
            name="email"
            placeholder="Email"
            className="w-full border border-sky-200 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-sky-400 transition"
            required
          />

          <input
            type="password"
            name="password"
            placeholder="Password"
            className="w-full border border-sky-200 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-sky-400 transition"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

          {/* Password checklist */}
          <div className="bg-sky-50 p-4 rounded-xl border border-sky-100 space-y-2">
            <CheckItem isValid={checks.length} label="รหัสผ่านต้องมีอย่างน้อย 8 ตัวอักษร" />
            <CheckItem
              isValid={checks.uppercase}
              label="มีตัวอักษรพิมพ์ใหญ่ (A-Z)"
            />
            <CheckItem
              isValid={checks.lowercase}
              label="มีตัวอักษรพิมพ์เล็ก (a-z)"
            />
          </div>

          <input
            type="password"
            name="confirmPassword"
            placeholder="Confirm Password"
            className="w-full border border-sky-200 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-sky-400 transition"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            required
          />

          <CheckItem isValid={checks.match} label="รหัสผ่านต้องตรงกัน" />

          {error && (
            <p className="text-sm text-red-500 text-center">{error}</p>
          )}

          <button
            type="submit"
            disabled={!isFormValid}
            className={`w-full py-3 rounded-xl font-medium text-white shadow-md transition duration-200
              ${
                isFormValid
                  ? "bg-sky-500 hover:bg-sky-600 hover:shadow-lg transform hover:scale-[1.02]"
                  : "bg-gray-400 cursor-not-allowed"
              }`}
          >
            Sign Up
          </button>

          <div className="text-center mt-4 text-sm text-gray-500">
            Already have an account?{" "}
            <span
              onClick={handleSignIn}
              className="text-sky-600 font-medium underline cursor-pointer hover:text-sky-700 transition"
            >
              Sign in
            </span>
          </div>

        </form>
      </div>
    </div>
  );
};

export default Signup;