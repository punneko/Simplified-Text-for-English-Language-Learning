import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Simplifier from "./pages/Simplifier";
import Result from "./pages/Result";
import History from "./pages/History";
import Manual from "./pages/Manual";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/simplifier" element={<Simplifier />} />
        <Route path="/result" element={<Result />} />
        <Route path="/history" element={<History />} />
        <Route path="/manual" element={<Manual />} />
      </Routes>
    </Router>
  );
}

export default App;
