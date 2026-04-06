import React from "react";
import { useNavigate } from "react-router-dom";
import { GoogleLogin } from "@react-oauth/google";

const Login = () => {
  const navigate = useNavigate();

  const handleLoginSubmit = (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const email = formData.get("email");
    const password = formData.get("password");

    fetch("http://localhost:5000/api/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data?.user_id) {
          localStorage.setItem("user_id", data.user_id);
          localStorage.setItem("name", data.name);
          localStorage.setItem("email", data.email);
          navigate("/simplifier");
        } else {
          alert(data.error || "Login failed");
        }
      })
      .catch(() => alert("Something went wrong"));
  };

  const handleSignUp = () => {
    navigate("/signup");
  };

  return (
    <div className="fredoka-font min-h-screen flex items-center justify-center bg-gradient-to-b from-sky-200 via-blue-100 to-white">
      
      <div className="bg-white/90 backdrop-blur-md p-10 rounded-3xl shadow-xl w-full max-w-sm border border-sky-100">
        
        <h2 className="text-3xl font-bold mb-8 text-center text-grey-800">
          Welcome!
        </h2>

        <form onSubmit={handleLoginSubmit} className="space-y-5">
          
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
            required
          />

          <button
            type="submit"
            className="w-full bg-sky-500 text-white py-3 rounded-xl font-medium shadow-md hover:bg-sky-600 hover:shadow-lg transform hover:scale-[1.02] transition duration-200"
          >
            Sign In
          </button>

          <div className="flex items-center my-4">
            <div className="flex-grow h-px bg-sky-200"></div>
            <span className="px-3 text-sm text-gray-400">or</span>
            <div className="flex-grow h-px bg-sky-200"></div>
          </div>

          <div className="flex justify-center">
            <GoogleLogin
              onSuccess={(response) => {
                if (!response.credential)
                  return alert("No credential received from Google");

                fetch("http://localhost:5000/api/auth/google-login", {
                  method: "POST",
                  headers: { "Content-Type": "application/json" },
                  body: JSON.stringify({ credential: response.credential }),
                })
                  .then((res) => res.json())
                  .then((data) => {
                    if (data?.user_id) {
                      localStorage.setItem("user_id", data.user_id);
                      localStorage.setItem("name", data.name);
                      localStorage.setItem("email", data.email);
                      localStorage.setItem("token", data.token);
                      navigate("/simplifier");
                    } else {
                      alert(data?.error || "Google login failed");
                    }
                  })
                  .catch(() => alert("Something went wrong"));
              }}
              onError={() => alert("Google login failed")}
            />
          </div>

          <div className="text-center mt-4 text-sm text-gray-500">
            Don’t have an account?{" "}
            <span
              onClick={handleSignUp}
              className="text-sky-600 font-medium underline cursor-pointer hover:text-sky-700 transition"
            >
              Sign up here
            </span>
          </div>

        </form>
      </div>
    </div>
  );
};

export default Login;